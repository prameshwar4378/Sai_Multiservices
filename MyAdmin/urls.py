from django.urls import path
from .views import * 

urlpatterns = [ 
    path('dashboard', dashboard, name="admin_dashboard"), 
 
    path('photo_gallery_category_list', photo_gallery_category_list, name="photo_gallery_category_list"), 
    path('create_photo_category_for_gallery', create_photo_category_for_gallery, name="create_photo_category_for_gallery"), 
    path('delete_category/<int:id>', delete_category, name="delete_category"), 

    path('photo_gallery_list', photo_gallery_list, name="photo_gallery_list"), 
    path('create_photo_for_gallery', create_photo_for_gallery, name="create_photo_for_gallery"), 
    path('delete_photo_from_gallery/<int:id>', delete_photo_from_gallery, name="delete_photo_from_gallery"), 
    # video Gallary
    path('video_gallery_list', video_gallery_list, name="video_gallery_list"), 
    path('create_video_for_gallery', create_video_for_gallery, name="create_video_for_gallery"), 
    path('delete_video_from_gallery/<int:id>', delete_video_from_gallery, name="admin_delete_video_from_gallery"), 

    path('enquiry_list', enquiry_list, name="admin_enquiry_list"), 
    path('delete_enquiry/<int:id>', delete_enquiry, name="admin_delete_enquiry"), 

    path('product_list', product_list, name="admin_product_list"), 
    path('update_product/<int:id>', update_product, name="admin_update_product"), 
    path('delete_product/<int:id>', delete_product, name="admin_delete_product"), 

]
