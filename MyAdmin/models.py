from django.db import models
import os
# Create your models here.
    
class PhotoGalleryCategories(models.Model):
    category_name = models.CharField(max_length=255) 
 
    def __str__(self):
        return f"{self.category_name}"

class PhotoGallery(models.Model):
    category = models.ForeignKey(PhotoGalleryCategories, on_delete=models.CASCADE, related_name='photos')
    caption = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="photo_gallery/")
    is_show_on_home_page = models.BooleanField(null=True)

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(PhotoGallery, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.caption} Image"

class VideoGallery(models.Model): 
    caption = models.CharField(max_length=255, blank=True, null=True)
    video_link = models.CharField(blank=True, null=True, help_text="Enter YouTube video link", max_length=255)
    thumbnail= models.ImageField(upload_to="video_thumnails/", null=True, blank=True)
  


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"






class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

from django.utils.text import slugify

class Product(models.Model):
    # Basic Info
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    catolouge = models.FileField(upload_to="products/media/", blank=True, null=True)
    product_image = models.ImageField(upload_to="products/media/", blank=True, null=True)
    slug = models.SlugField(unique=False, blank=True)  # New slug field

    class Meta:
        verbose_name = "Product"         
        verbose_name_plural = "Products" 
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Save the instance first to get an ID
        super().save(*args, **kwargs)

        # Create slug with title + id
        expected_slug = f"{slugify(self.title)}-{self.id}"

        if self.slug != expected_slug:
            self.slug = expected_slug
            super().save(update_fields=['slug'])

class ProductMedia(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default=IMAGE)
    file = models.FileField(upload_to="products/media/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)  # For external video or image links
    order = models.PositiveIntegerField(default=0)  # to manage slider order

    def __str__(self):
        return f"{self.product.title} - {self.media_type}"

    class Meta:
        verbose_name = "Product Media"         
        verbose_name_plural = "Product Media" 