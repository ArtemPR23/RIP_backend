from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='artifact_list'),
    path('artifact/<int:artifact_id>/', views.artifact_detail, name='artifact_detail'),
    path('artifact/<int:artifact_id>/delete/', views.delete_artifact, name="delete_artifact"),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    
    path('request/<int:artifact_id>/add_to_artifact/', views.add_artifact_to_draft_request, name="add_artifact_to_draft_request"),
    path('request/<int:artifact_id>/del_to_artifact/', views.del_artifact_to_draft_request, name="del_artifact_to_draft_request"),

]