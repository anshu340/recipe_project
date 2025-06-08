from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/new/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='recipes/logout.html',
        http_method_names=['get', 'post']
    ), name='logout'),
    path('register/', views.register, name='register'),
    
    # User profile URLs
    path('user/<str:username>/recipes/', views.user_recipes, name='user_recipes'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    
    # About Us and Bookmark URLs
    path('about/', views.about, name='about'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('recipes/<int:recipe_id>/toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('recipes/<int:recipe_id>/remove-bookmark/', views.remove_bookmark, name='remove_bookmark'),
]