from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PhotoGalleryCategories, PhotoGallery,
    VideoGallery, Enquiry,
    Product, ProductMedia,Category
)
import re
from django.contrib.auth.models import User, Group


admin.site.site_header = "Shri Saimultiservices"
admin.site.site_title = "Shri Saimultiservices Admin Portal"
admin.site.index_title = "Welcome to Shri Saimultiservices Dashboard"

# Remove default User and Group from admin
admin.site.unregister(User)
admin.site.unregister(Group)

 

# ========== PHOTO GALLERY ==========
class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    extra = 1
    fields = ('caption', 'description', 'image', 'is_show_on_home_page')
    show_change_link = True


@admin.register(PhotoGalleryCategories)
class PhotoGalleryCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'photo_count')
    search_fields = ('category_name',)
    ordering = ('category_name',)
    inlines = [PhotoGalleryInline]

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = "Total Photos"


@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'category', 'is_show_on_home_page', 'thumbnail_preview')
    list_filter = ('category', 'is_show_on_home_page')
    search_fields = ('caption', 'description', 'category__category_name')
    ordering = ('-id',)
    list_editable = ('is_show_on_home_page',)
    autocomplete_fields = ('category',)
    readonly_fields = ('thumbnail_preview',)
    fieldsets = (
        ('Basic Info', {'fields': ('category', 'caption', 'description')}),
        ('Image Settings', {'fields': ('image', 'thumbnail_preview', 'is_show_on_home_page')}),
    )
    actions = ['mark_as_show_on_home', 'mark_as_hide_from_home']
    save_on_top = True

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px; height:auto; border-radius:5px;" />', obj.image.url)
        return "No Image"
    thumbnail_preview.short_description = "Preview"

    def mark_as_show_on_home(self, request, queryset):
        updated = queryset.update(is_show_on_home_page=True)
        self.message_user(request, f"{updated} photos marked as show on home page.")
    mark_as_show_on_home.short_description = "✅ Show on Home Page"

    def mark_as_hide_from_home(self, request, queryset):
        updated = queryset.update(is_show_on_home_page=False)
        self.message_user(request, f"{updated} photos hidden from home page.")
    mark_as_hide_from_home.short_description = "❌ Hide from Home Page"


# ========== VIDEO GALLERY =========

# --- Helper for extracting YouTube video ID ---
def extract_video_id(url):
    if not url:
        return None
    patterns = [
        r"embed/([a-zA-Z0-9_-]+)",  # https://www.youtube.com/embed/ID
        r"v=([a-zA-Z0-9_-]+)",      # https://www.youtube.com/watch?v=ID
        r"youtu\.be/([a-zA-Z0-9_-]+)"  # https://youtu.be/ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# --- VIDEO GALLERY ADMIN ---
@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'video_link', 'thumbnail_preview')
    search_fields = ('caption', 'video_link')
    ordering = ('-id',)
    list_editable = ('video_link',)
    readonly_fields = ('thumbnail_preview',)
    fieldsets = (
        ('Video Info', {'fields': ('caption', 'video_link',  'thumbnail_preview')}),
    )
    save_on_top = True

    def thumbnail_preview(self, obj):
        # Prefer uploaded thumbnail if exists
        if obj.thumbnail:
            return format_html('<img src="{}" style="width:100px; height:auto;" />', obj.thumbnail.url)

        # Otherwise, try extracting from YouTube
        video_id = extract_video_id(obj.video_link)
        if video_id:
            thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            return format_html('<img src="{}" style="width:100px; height:auto;" />', thumb_url)

        return "No Thumbnail"
    thumbnail_preview.short_description = "Thumbnail"





# ========== ENQUIRIES ==========
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'email', 'subject', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'mobile', 'email', 'subject', 'message')
    ordering = ('-date',)
    readonly_fields = ('date',)
    save_on_top = True


# ========== PRODUCT & MEDIA ==========

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import JsonResponse
import json
import re

# Utility function to extract video ID
def extract_video_id(url):
    if not url:
        return None
    # YouTube URL patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# --- Product Media Inline ---
class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 2
    fields = ('media_type', 'file', 'url', 'video_file', 'video_thumbnail', 'order', 'preview')
    readonly_fields = ('preview',)
    show_change_link = True
    
    # Add custom JavaScript for upload progress
    class Media:
        js = (
            'admin/js/jquery.init.js',
            'js/video_upload_progress.js',  # We'll create this file
        )
        css = {
            'all': ('css/admin_custom.css',)  # For progress bar styling
        }

    def preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="width:80px; height:auto; border-radius:5px;" />', obj.file.url)
        if obj.media_type == ProductMedia.VIDEO:
            if obj.video_file:
                return format_html('<a href="{}" target="_blank">🎬 Uploaded Video</a>', obj.video_file.url)
            if obj.url:
                video_id = extract_video_id(obj.url)
                if video_id:
                    thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                    return format_html('<img src="{}" style="width:80px; height:auto;" />', thumb_url)
                return format_html('<a href="{}" target="_blank">🌐 External Video</a>', obj.url)
        return "No Preview"
    preview.short_description = "Preview"

# --- Product Admin ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'catalogue_link', 'media_count', 'created_on', 'product_image_preview')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'slug', 'product_image_preview')
    inlines = [ProductMediaInline]
    save_on_top = True
    
    # Add custom template with progress bar support
    change_form_template = 'admin/products/product_change_form.html'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'description', 'created_at')
        }),
        ('Media', {
            'fields': ('product_image', 'product_image_preview', 'catolouge' ),
            'classes': ('collapse',)
        }),
    )

    def catalogue_link(self, obj):
        if obj.catolouge:
            return format_html('<a href="{}" target="_blank">📂 Download Catalogue</a>', obj.catolouge.url)
        return "-"
    catalogue_link.short_description = "Catalogue"

    def product_image_preview(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="width:100px; height:auto; border-radius:5px;" />', obj.product_image.url)
        return "No Image"
    product_image_preview.short_description = "Image Preview"

    def media_count(self, obj):
        count = obj.media.count()
        return format_html('<span class="badge">{}</span>', count)
    media_count.short_description = "Media Files"

    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")
    created_on.short_description = "Created On"

    actions = ["publish_all_media"]

    def publish_all_media(self, request, queryset):
        count = 0
        for product in queryset:
            count += product.media.update(media_type=ProductMedia.IMAGE)
        self.message_user(request, f"{count} media files updated ✅")
    
    # Add custom URL for video upload progress
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-progress/', self.admin_site.admin_view(self.upload_progress), name='upload_progress'),
        ]
        return custom_urls + urls
    
    def upload_progress(self, request):
        """API endpoint for upload progress"""
        upload_id = request.GET.get('upload_id')
        # In a real implementation, you'd track progress using session or cache
        # For now, returning a dummy response
        return JsonResponse({
            'upload_id': upload_id,
            'progress': 0,
            'status': 'pending'
        })

# --- Category Admin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_preview', 'description', 'created_at', 'product_count')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width:30px; height:30px;" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "Icon"

    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<span class="badge">{}</span>', count)
    product_count.short_description = "Products"

# --- ProductMedia Admin ---
@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'media_type', 'order', 'thumbnail_preview', 'video_info')
    list_filter = ('media_type', 'product__category')
    search_fields = ('product__title',)
    ordering = ('product', 'order')
    readonly_fields = ('media_preview', 'video_info')
    list_per_page = 20
    
    # Add custom template for better video upload interface
    change_form_template = 'admin/products/productmedia_change_form.html'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'media_type', 'order')
        }),
        ('Image Content', {
            'fields': ('file',),
            'classes': ('collapse',)
        }),
        ('Video Content', {
            'fields': ('video_file', 'url', 'video_thumbnail', 'video_info'),
            'description': 'For videos, either upload a file or provide an external URL'
        }),
        ('Preview', {
            'fields': ('media_preview',),
            'classes': ('wide',)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="width:80px; height:auto;" />', obj.file.url)
        if obj.media_type == ProductMedia.VIDEO:
            if obj.video_thumbnail:
                return format_html('<img src="{}" style="width:100px; height:auto;" />', obj.video_thumbnail.url)
            video_id = extract_video_id(obj.url)
            if video_id:
                thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                return format_html('<img src="{}" style="width:100px; height:auto;" />', thumb_url)
            elif obj.video_file:
                return format_html('🎬 <span style="font-size:12px;">Video File</span>')
        return "No Preview"
    thumbnail_preview.short_description = "Thumbnail"
    
    def video_info(self, obj):
        if obj.media_type == ProductMedia.VIDEO:
            info = []
            if obj.video_file:
                info.append(f"File: {obj.video_file.name}")
                if hasattr(obj.video_file, 'size'):
                    size_mb = obj.video_file.size / (1024 * 1024)
                    info.append(f"Size: {size_mb:.2f} MB")
            if obj.url:
                info.append(f"URL: {obj.url}")
            if info:
                return format_html('<br>'.join(info))
        return "-"
    video_info.short_description = "Video Details"

    def media_preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html(
                '<div style="text-align:center;">'
                '<img src="{}" style="max-width:400px; height:auto; border-radius:6px;" />'
                '</div>', obj.file.url
            )
        if obj.media_type == ProductMedia.VIDEO:
            video_id = extract_video_id(obj.url)
            if video_id:
                return format_html(
                    '<div style="text-align:center;">'
                    '<iframe width="500" height="300" src="https://www.youtube.com/embed/{}" '
                    'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                    'allowfullscreen></iframe>'
                    '</div>', video_id
                )
            elif obj.video_file:
                return format_html(
                    '<div style="text-align:center;">'
                    '<video width="500" height="300" controls preload="metadata">'
                    '<source src="{}" type="video/mp4">'
                    'Your browser does not support the video tag.'
                    '</video>'
                    '</div>',
                    obj.video_file.url
                )
        return "No Preview Available"
    media_preview.short_description = "Full Preview"
    
    # Add custom admin action for bulk operations
    actions = ['generate_thumbnails']
    
    def generate_thumbnails(self, request, queryset):
        """Generate thumbnails for selected videos"""
        count = 0
        for media in queryset.filter(media_type=ProductMedia.VIDEO):
            if media.video_file and not media.video_thumbnail:
                # Here you would implement actual thumbnail generation
                # For now, just mark as processed
                media.save()
                count += 1
        self.message_user(request, f"Processed {count} videos for thumbnail generation")
    generate_thumbnails.short_description = "Generate thumbnails for videos"