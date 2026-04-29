
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('image_detail/', views.image_detail, name='image_detail'),
    path('delete/', views.delete, name='delete'),

    path('api/images/', views.api_upload_image, name='api_upload_image'),
    path('api/images/<int:image_id>/', views.api_get_image, name='api_get_image'),
    path('api/images/<int:image_id>/delete/', views.api_delete_image, name='api_delete_image'),
]
