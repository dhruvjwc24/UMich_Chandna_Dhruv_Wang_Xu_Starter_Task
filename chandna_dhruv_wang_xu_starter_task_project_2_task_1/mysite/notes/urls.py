# --- File: notes/urls.py ---

from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('upload/', views.upload_pdf_view, name='upload_pdf'),
    path('pdf/<int:article_id>/', views.view_pdf, name='view_pdf'),
    path('save-annotation/', views.save_annotation, name='save_annotation'),
    path('delete-annotation/', views.delete_annotation, name='delete_annotation'),
    path('update-note/', views.update_note, name='update_note'),
]
