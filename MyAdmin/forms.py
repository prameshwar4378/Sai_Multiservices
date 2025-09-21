from django import forms
from .models import *
from django.contrib.auth.forms  import AuthenticationForm
from django_summernote.widgets import SummernoteWidget
from django.core.exceptions import ValidationError
from PIL import Image
import io


class login_form(AuthenticationForm):
    username=forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'username','placeholder':'Enter Username'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'username','placeholder':'Enter Password'}))


class PhotoGalleryCategoriesForm(forms.ModelForm):
    class Meta:
        model = PhotoGalleryCategories
        fields = ['category_name'] 


class PhotoGalleryForm(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        fields = ['category','caption', 'image','description','is_show_on_home_page']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',  # Optional Bootstrap class for styling
                'rows': 4,  # Set the height to 4 lines
                'placeholder': 'Enter a short description...',  # Optional placeholder
            }),
        }


class VideoGalleryForm(forms.ModelForm):
    class Meta:
        model = VideoGallery
        fields = ['caption', 'video_link']




from .models import Product,  ProductMedia
from django import forms
from .models import Product, ProductMedia


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "catolouge",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter product title"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter product description"}),
            "catolouge": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ["media_type", "file", "url", "order"]
        widgets = {
            "media_type": forms.Select(attrs={"class": "form-select"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"placeholder": "https://example.com/video-or-image"}),
            "order": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
        }
