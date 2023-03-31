# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('community/', views.community, name='community'),
    path('community/<int:news_id>/', views.community, name='community_with_id'),
    path('addnews/', views.add_news, name='add_news'),
    path('submit-news/', views.submit_news, name='submit_news'),
    path('delete_all_news/', views.delete_all_news, name='delete_all_news'),
    path('', views.index, name='index'),
    path('login_register/', views.login_register, name='login_register'),
]