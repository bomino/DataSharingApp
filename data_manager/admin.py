from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, DataFile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_by', 'uploaded_at', 'validated', 'version')
    list_filter = ('validated', 'uploaded_at', 'uploaded_by__role')
    search_fields = ('file', 'uploaded_by__username', 'description')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('uploaded_at', 'version')
    
    actions = ['mark_as_validated', 'increment_version']
    
    def file_name(self, obj):
        return obj.file.name.split('/')[-1]
    file_name.short_description = _('File Name')
    
    def mark_as_validated(self, request, queryset):
        updated = queryset.update(validated=True)
        self.message_user(request, _(
            f'{updated} files marked as validated.'
        ))
    mark_as_validated.short_description = _('Mark selected files as validated')
    
    def increment_version(self, request, queryset):
        for obj in queryset:
            obj.version += 1
            obj.save()
        self.message_user(request, _(
            f'Version incremented for {queryset.count()} files.'
        ))
    increment_version.short_description = _('Increment version number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'analyst':
            return qs.filter(uploaded_by=request.user)
        return qs.none()