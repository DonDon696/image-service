
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('image_detail/', views.image_detail, name='image_detail'),
    path('delete/', views.delete, name='delete'),

]
