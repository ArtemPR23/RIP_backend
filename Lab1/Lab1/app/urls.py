from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='artifact_list'),
    path('artifact/<int:artifact_id>/', views.artifact_detail, name='artifact_detail'),
    path('citation_request/<int:request_id>/', views.request_detail, name='request_detail'),
]