from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('filter_results/', views.filter_results, name='filter_results'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_book/', views.add_book, name='add_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('save_edit_user/<int:user_id>/', views.save_edit_user, name='save_edit_user'),
    path('save_edit_book/<int:book_id>/', views.save_edit_book, name='save_edit_book'),
]