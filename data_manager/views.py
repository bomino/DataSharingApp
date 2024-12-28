from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import pandas as pd
from .models import DataFile
from .forms import DataFileUploadForm
from .serializers import DataFileSerializer
from .permissions import IsAnalystOrAdmin
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import SharedFile, DataFile, User


@login_required
def home(request):
    # Only get stats for admin and analyst
    if request.user.is_superuser or request.user.role == 'analyst':
        total_files = DataFile.objects.count()
        my_files = DataFile.objects.filter(uploaded_by=request.user).count()
        
        # Get recent activity (last 7 days)
        last_week = timezone.now() - timedelta(days=7)
        recent_uploads = DataFile.objects.filter(uploaded_at__gte=last_week).count()
        
        # Get validation stats
        valid_files = DataFile.objects.filter(validated=True).count()
        pending_files = DataFile.objects.filter(validated=False).count()
        validation_rate = (valid_files / total_files * 100) if total_files > 0 else 0
        
        # Get sharing stats
        now = timezone.now()
        sharing_stats = {
            'shared_by_me': SharedFile.objects.filter(
                shared_by=request.user,
                active=True,
                expiry_date__gt=now
            ).count(),
            'shared_with_me': SharedFile.objects.filter(
                shared_with=request.user,
                active=True,
                expiry_date__gt=now
            ).count(),
            'expiring_soon': SharedFile.objects.filter(
                shared_by=request.user,
                active=True,
                expiry_date__gt=now,
                expiry_date__lte=now + timedelta(days=2)
            ).count(),
            'recent_shares': SharedFile.objects.filter(
                shared_by=request.user,
                shared_at__gte=last_week
            ).count(),
        }
        
        context = {
            'total_files': total_files,
            'my_files': my_files,
            'recent_uploads': recent_uploads,
            'validation_stats': {
                'valid': valid_files,
                'pending': pending_files,
                'rate': round(validation_rate, 1)
            },
            'sharing_stats': sharing_stats,
        }
    else:
        context = {}
        
    return render(request, 'data_manager/home.html', context)

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DataFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.uploaded_by = request.user
            
            # Add validation here
            try:
                file_obj = request.FILES['file']
                if file_obj.name.endswith('.csv'):
                    df = pd.read_csv(file_obj)
                elif file_obj.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_obj)
                else:
                    raise ValidationError(_('Unsupported file format'))

                # Set validated to True if validation passes
                file_instance.validated = True
                file_instance.save()
                messages.success(request, _('File uploaded successfully.'))
                return redirect('file_list')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = DataFileUploadForm()
    return render(request, 'data_manager/upload.html', {'form': form})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(DataFile, id=file_id)
    
    # Check if user has permission to delete
    if request.user.is_superuser or (request.user.role == 'analyst' and file.uploaded_by == request.user):
        file_name = file.file.name
        file.file.delete()  # Delete the actual file
        file.delete()       # Delete the database record
        messages.success(request, f'File "{file_name}" has been deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this file.')
    
    return redirect('file_list')

@login_required
def file_list(request):
    if request.user.is_superuser:
        files = DataFile.objects.all()

    else:
        files = DataFile.objects.filter(uploaded_by=request.user)
    return render(request, 'data_manager/file_list.html', {'files': files})

@login_required
def shared_files(request):
    # Deactivate expired shares
    SharedFile.objects.filter(
        expiry_date__lte=timezone.now(),
        active=True
    ).update(active=False)

    context = {
        'shared_by_me': SharedFile.objects.filter(
            shared_by=request.user,
            active=True,
            expiry_date__gt=timezone.now()
        ),
        'shared_with_me': SharedFile.objects.filter(
            shared_with=request.user,
            active=True,
            expiry_date__gt=timezone.now()
        ),
        'my_files': DataFile.objects.filter(uploaded_by=request.user),
        'available_users': User.objects.filter(
            ~Q(id=request.user.id),
            is_active=True
        ).exclude(
            id__in=SharedFile.objects.filter(
                shared_by=request.user,
                active=True,
                expiry_date__gt=timezone.now()
            ).values('shared_with')
        )
    }
    return render(request, 'data_manager/shared_files.html', context)

@login_required
def share_file(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        user_id = request.POST.get('user_id')
        expiry_days = int(request.POST.get('expiry_days', 7))
        
        try:
            file = DataFile.objects.get(id=file_id, uploaded_by=request.user)
            user_to_share = User.objects.get(id=user_id)
            
            # Check if already shared (active or inactive)
            existing_share = SharedFile.objects.filter(
                file=file,
                shared_with=user_to_share
            ).first()
            
            if existing_share:
                if existing_share.active and existing_share.expiry_date and existing_share.expiry_date > timezone.now():
                    messages.warning(request, _('File is already shared with this user'))
                else:
                    # Reactivate and update expiry
                    existing_share.active = True
                    existing_share.expiry_date = timezone.now() + timedelta(days=expiry_days)
                    existing_share.shared_at = timezone.now()  # Reset share date
                    existing_share.save()
                    messages.success(
                        request,
                        _(f'File reshared with {user_to_share.username} (expires in {expiry_days} days)')
                    )
            else:
                # Create new share
                SharedFile.objects.create(
                    file=file,
                    shared_by=request.user,
                    shared_with=user_to_share,
                    expiry_date=timezone.now() + timedelta(days=expiry_days)
                )
                messages.success(
                    request,
                    _(f'File shared with {user_to_share.username} (expires in {expiry_days} days)')
                )
                
        except (DataFile.DoesNotExist, User.DoesNotExist):
            messages.error(request, _('Invalid file or user selection'))
            
    return redirect('shared_files')

@login_required
def unshare_file(request, share_id):
    if request.method == 'POST':
        share = get_object_or_404(
            SharedFile,
            id=share_id,
            shared_by=request.user,
            active=True
        )
        share.active = False
        share.save()
        
        messages.success(
            request,
            _(f'File access removed for {share.shared_with.username}')
        )
        return JsonResponse({'status': 'success'})
        
    return JsonResponse({'status': 'error'}, status=400)





class DataFileViewSet(viewsets.ModelViewSet):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAnalystOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DataFile.objects.all()
        if self.request.user.role == 'analyst':
            return DataFile.objects.filter(uploaded_by=self.request.user)
        return DataFile.objects.none()

    def perform_create(self, serializer):
        file_obj = self.request.FILES['file']
        
        try:
            if file_obj.name.endswith('.csv'):
                df = pd.read_csv(file_obj)
            elif file_obj.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_obj)
            else:
                raise ValidationError(_('Unsupported file format'))

            if self.validate_data(df):
                serializer.save(
                    uploaded_by=self.request.user,
                    validated=True
                )
            else:
                raise ValidationError(_('Invalid data format'))

        except Exception as e:
            raise ValidationError(f'Error processing file: {str(e)}')

    def validate_data(self, df):
        required_columns = ['date', 'value', 'category']
        return all(col in df.columns for col in required_columns)

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        data_file = self.get_object()
        try:
            file_obj = data_file.file
            if file_obj.name.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                df = pd.read_excel(file_obj)

            if self.validate_data(df):
                data_file.validated = True
                data_file.save()
                return Response({'status': 'file validated'})
            return Response(
                {'error': 'invalid data format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )