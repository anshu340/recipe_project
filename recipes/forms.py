from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'cooking_time', 'difficulty', 'servings', 'image', 'category']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter each ingredient on a new line'}),
            'instructions': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Enter each step on a new line'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Add custom help text and labels
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'
        
        # Add classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

