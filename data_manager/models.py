from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
import os

class User(AbstractUser):
    BASIC = 'basic'
    ANALYST = 'analyst'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (BASIC, _('Basic User')),
        (ANALYST, _('Data Analyst')),
        (ADMIN, _('Administrator')),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=BASIC,
        verbose_name=_('User Role')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        permissions = [
            ("can_upload_data", _("Can upload data files")),
            ("can_analyze_data", _("Can analyze data")),
            ("can_manage_users", _("Can manage users")),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class DataFile(models.Model):
    def get_file_path(instance, filename):
        # Get file extension and base name
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        
        # Clean the base name to be URL-friendly
        base_name = slugify(base_name)
        
        # Get latest version for this user and base filename
        latest = DataFile.objects.filter(
            uploaded_by=instance.uploaded_by,
            file__icontains=base_name
        ).order_by('-version').first()
        
        version = (latest.version + 1) if latest else 1
        
        # Format: username/YYYY-MM-DD/filename_v1.ext
        return f'uploads/{instance.uploaded_by.username}/{timezone.now():%Y-%m-%d}/{base_name}_v{version}{ext}'

    file = models.FileField(
        upload_to=get_file_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['csv', 'xlsx', 'xls']
        )],
        verbose_name=_('File')
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploads',
        verbose_name=_('Uploaded by')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Upload date')
    )
    validated = models.BooleanField(
        default=False,
        verbose_name=_('Validation status')
    )
    version = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Version')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )

    class Meta:
        verbose_name = _('Data File')
        verbose_name_plural = _('Data Files')
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_filename()} (v{self.version})"
        
    def get_filename(self):
        """Returns a clean filename without the path"""
        return os.path.basename(self.file.name)

    def get_file_extension(self):
        """Returns the file extension"""
        return os.path.splitext(self.file.name)[1].lower()

    def get_file_icon(self):
        """Returns the appropriate Bootstrap icon class based on file type"""
        if self.get_file_extension() == '.csv':
            return 'bi-filetype-csv text-success'
        elif self.get_file_extension() in ['.xlsx', '.xls']:
            return 'bi-filetype-xlsx text-primary'
        return 'bi-file-earmark-text'

class SharedFile(models.Model):
    file = models.ForeignKey(
        DataFile,
        on_delete=models.CASCADE,
        related_name='shares',
        verbose_name=_('File')
    )
    shared_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_files',
        verbose_name=_('Shared by')
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_files',
        verbose_name=_('Shared with')
    )
    shared_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Share date')
    )
    expiry_date = models.DateTimeField(
        verbose_name=_('Expiry date'),
        null=True,
        blank=True
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )

    class Meta:
        verbose_name = _('Shared File')
        verbose_name_plural = _('Shared Files')
        ordering = ['-shared_at']
        unique_together = ['file', 'shared_with']

    def __str__(self):
        return f"{self.file.get_filename()} - shared with {self.shared_with.username}"

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            # Set default expiry to 7 days from now
            self.expiry_date = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expiry_date if self.expiry_date else False

    @property
    def time_remaining(self):
        if self.expiry_date and not self.is_expired:
            remaining = self.expiry_date - timezone.now()
            days = remaining.days
            hours = remaining.seconds // 3600
            if days > 0:
                return f"{days}d {hours}h remaining"
            return f"{hours}h remaining"
        return "Expired"