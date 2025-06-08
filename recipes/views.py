from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Recipe, Category, Bookmark
from .forms import RecipeForm, CustomUserCreationForm

def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'recipes/home.html', {
        'recipes': recipes,
        'categories': categories,
    })

def recipe_list(request):
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search_query = request.GET.get('search')
    
    recipes = Recipe.objects.all()
    
    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)
    
    categories = Category.objects.all()
    
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_difficulty': difficulty,
        'search_query': search_query,
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_owner = recipe.author == request.user if request.user.is_authenticated else False
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'is_owner': is_owner,
        'is_bookmarked': is_bookmarked
    })

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Add New Recipe'
    })

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if user is the author
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('recipe_detail', recipe_id=recipe.id)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Edit Recipe',
        'recipe': recipe
    })

@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if user is the author
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to delete this recipe.")
        return redirect('recipe_detail', recipe_id=recipe.id)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'recipes/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'recipes/category_detail.html', {
        'category': category,
        'recipes': recipes
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})

def user_recipes(request, username):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'recipes/user_recipes.html', {
        'recipes': recipes,
        'profile_user': user
    })

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/my_recipes.html', {
        'recipes': recipes
    })

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        subject = f'Contact Form Message from {name}'
        email_message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
        try:
            send_mail(
                subject,
                email_message,
                email,  # From email
                [settings.DEFAULT_FROM_EMAIL],  # To email
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        
        return redirect('about')
    
    return render(request, 'recipes/about.html')

@login_required
def bookmarks(request):
    bookmarked_recipes = Recipe.objects.filter(bookmarked_by__user=request.user)
    return render(request, 'recipes/bookmarks.html', {
        'bookmarked_recipes': bookmarked_recipes
    })

@login_required
def toggle_bookmark(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, recipe=recipe)
        
        if not created:
            # If bookmark already existed, remove it
            bookmark.delete()
            return JsonResponse({'status': 'removed'})
        
        return JsonResponse({'status': 'added'})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def remove_bookmark(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Bookmark.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

