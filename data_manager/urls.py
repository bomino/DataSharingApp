

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'files', views.DataFileViewSet, basename='datafile')

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('files/', views.file_list, name='file_list'),
    path('api/', include(router.urls)),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('shared/', views.shared_files, name='shared_files'),
    path('share/', views.share_file, name='share_file'),
    path('unshare/<int:share_id>/', views.unshare_file, name='unshare_file'),
]