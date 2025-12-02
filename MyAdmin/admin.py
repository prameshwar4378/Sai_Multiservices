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


# --- Product Media Inline ---
class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 2
    fields = ('media_type', 'file', 'url', 'order', 'preview')
    readonly_fields = ('preview',)
    show_change_link = True

    def preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="width:80px; height:auto; border-radius:5px;" />', obj.file.url)
        if obj.media_type == ProductMedia.VIDEO:
            if obj.file:
                return format_html('<a href="{}" target="_blank">🎬 Uploaded Video</a>', obj.file.url)
            if obj.url:
                return format_html('<a href="{}" target="_blank">🌐 External Video</a>', obj.url)
        return "No Preview"
    preview.short_description = "Preview"

# --- Product Admin ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'catalogue_link', 'media_count', 'created_on', 'product_image')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    inlines = [ProductMediaInline]
    save_on_top = True

    def catalogue_link(self, obj):
        if obj.catolouge:
            return format_html('<a href="{}" target="_blank">📂 Download</a>', obj.catolouge.url)
        return "-"
    catalogue_link.short_description = "Catalogue"

    def media_count(self, obj):
        return obj.media.count()
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

# --- Category Admin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','icon', 'description', 'created_at', 'product_count')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"

# --- ProductMedia Admin ---
@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'media_type', 'order', 'thumbnail_preview')
    list_filter = ('media_type',)
    search_fields = ('product__title',)
    ordering = ('product', 'order')
    readonly_fields = ('media_preview',)

    def thumbnail_preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="width:80px; height:auto;" />', obj.file.url)
        if obj.media_type == ProductMedia.VIDEO:
            video_id = extract_video_id(obj.url)
            if video_id:
                thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                return format_html('<img src="{}" style="width:100px; height:auto;" />', thumb_url)
            elif obj.file:
                return "🎬 Video File"
        return "No Preview"
    thumbnail_preview.short_description = "Thumbnail"

    def media_preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="max-width:400px; height:auto; border-radius:6px;" />', obj.file.url)
        if obj.media_type == ProductMedia.VIDEO:
            video_id = extract_video_id(obj.url)
            if video_id:
                return format_html(
                    '<iframe width="400" height="250" src="https://www.youtube.com/embed/{}" '
                    'frameborder="0" allowfullscreen></iframe>', video_id
                )
            elif obj.file:
                return format_html(
                    '<video width="400" height="250" controls>'
                    '<source src="{}" type="video/mp4">Your browser does not support video.</video>',
                    obj.file.url
                )
        return "No Preview"
    media_preview.short_description = "Full Preview"