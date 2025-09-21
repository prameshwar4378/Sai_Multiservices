 
from django.urls import path
from Website.views import  *
urlpatterns = [
    path('contact-us', contact_us, name="website_contact_us"),
    path('photos_gallary', web_photos_gallary, name="web_photos_gallary"),
    path('videos_gallary', web_videos_gallary, name="web_videos_gallary"),
    path('products', products, name="web_products"),
    path('product_details/<int:id>', product_details, name="web_product_details"),
    path('services', services, name="web_services"),
    path('faq', faq, name="web_faq"),
    path('about_us', about_us, name="web_about_us"),
]