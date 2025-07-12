from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path("upload/", views.upload_pdf_view, name="upload_pdf"),
    path("pdf/<int:article_id>/", views.view_pdf, name="view_pdf"),
]