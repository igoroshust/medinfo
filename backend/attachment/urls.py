from django.urls import path

from attachment import views

urlpatterns = [
    path('', views.check_attachment, name='check_attachment'),
]
