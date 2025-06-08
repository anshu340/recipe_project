from django.contrib import admin
from .models import Recipe, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'cooking_time', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')

