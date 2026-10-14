from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('login/', views.user_login, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', views.user_logout, name='logout'),

    path('about/', views.about, name='about'),

    path('reservation/', views.reservation, name='reservation'),

    path('search/', views.search, name='search'),

    path(
        'category/<int:category_id>/',
        views.category_page,
        name='category'
    ),

    path(
        'article/<int:article_id>/',
        views.article_detail,
        name='article'
    ),

    path(
        'add_article/',
        views.add_article,
        name='add_article'
    ),

    path(
        'article/<int:article_id>/update/',
        views.update_article,
        name='update'
    ),

    path(
        'article/<int:article_id>/delete/',
        views.delete_article,
        name='delete'
    ),

    # =========================
    # FAVORITES
    # =========================

    path(
        'favorite/<int:article_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),

    path(
        'favorites/',
        views.favorites,
        name='favorites'
    ),

]