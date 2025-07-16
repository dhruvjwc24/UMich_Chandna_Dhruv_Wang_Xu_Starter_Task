# --- File: notes/urls.py ---

from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'), # in-use
    path('upload/', views.upload_pdf_view, name='upload_pdf'), # in-use
    path('pdf/<int:article_id>/', views.view_pdf, name='view_pdf'), # in-use
    path('api/save_annotation/', views.save_annotation, name='save_annotation'), # in-use
    path('api/save_note/', views.save_note, name='save_note'), # in-use
    path('api/delete_note_and_annotation/', views.delete_note_and_annotation, name='delete_note_and_annotation'), # in-use
    path('api/update-note/', views.update_note, name='update_note'),
    path('api/suggest_note/', views.suggest_note, name='suggest_note'), # in-use
]
