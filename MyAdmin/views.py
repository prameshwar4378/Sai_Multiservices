from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request): 
    lg_form=login_form() 
    if request.method=='POST': 
         
        if 'username' in request.POST: 
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                authlogin(request,user) 
                return redirect('/admin/dashboard',{'user',user})
            else:
                lg_form=login_form()
                messages.info(request,'Opps...! User does not exist... Please try again..!')
        else:
            print("Login Missing")

    return render(request,'login.html',{'form':lg_form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')

@login_required
def dashboard(request):
    enquiry_count = Enquiry.objects.count()
    context = {
        'enquiry_count' : enquiry_count,
    }

    return render(request,"admin_dashboard.html", context)
  
@login_required
def photo_gallery_category_list(request): 
    data = PhotoGalleryCategories.objects.all()
    form = PhotoGalleryCategoriesForm()
    return render(request, 'admin_photo_gallery_categories_list.html', {'form': form, "data":data})


@login_required
def create_photo_category_for_gallery(request):
    if request.method == 'POST':
        form = PhotoGalleryCategoriesForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"Category Added Success")
            return redirect('/admin/photo_gallery_category_list') 
        else:
            messages.error(request,"Form is not valid")
            return redirect('/admin/photo_gallery_category_list') 
             # Assuming you have a URL named 'list' for listing events
    else: 
            messages.error(request,"Form is not valid")
            return redirect('/admin/photo_gallery_category_list')  # Assuming you have a URL named 'list' for listing events


def delete_category(request,id):
    PhotoGalleryCategories.objects.get(id=id).delete()
    messages.success(request,"Category Deleted Success")
    return redirect("/admin/photo_gallery_category_list")



@login_required
def photo_gallery_list(request): 
    data = PhotoGallery.objects.all()
    form = PhotoGalleryForm()
    return render(request, 'admin_photo_gallery_list.html', {'form': form, "data":data})


@login_required
def create_photo_for_gallery(request):
    if request.method == 'POST':
        form = PhotoGalleryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"Photo Added Success")
            return redirect('/admin/photo_gallery_list') 
        else:
            messages.error(request,"Form is not valid")
            return redirect('/admin/photo_gallery_list') 
             # Assuming you have a URL named 'list' for listing events
    else: 
            messages.error(request,"Form is not valid")
            return redirect('/admin/photo_gallery_list')  # Assuming you have a URL named 'list' for listing events

 
def delete_photo_from_gallery(request,id):
    PhotoGallery.objects.get(id=id).delete()
    return redirect("/admin/photo_gallery_list")



import re

def extract_video_id(embed_url):
    match = re.search(r"embed/([a-zA-Z0-9_-]+)", embed_url)
    if match:
        return match.group(1)
    return None




@login_required
def video_gallery_list(request): 
    data = VideoGallery.objects.all()
    video_data=[]
    for embed_link in data:
        embed_url= embed_link.video_link
        if embed_url:
            video_id=extract_video_id(embed_url)
        
            if video_id:
                video_data.append(
                    {"thumbnail_url":f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                    "video_url":f"https://www.youtube.com/embed/{video_id}",
                    "id":embed_link.id} 
                )
    form = VideoGalleryForm()
    return render(request, 'admin_video_gallary_list.html', {'form': form, "video_data":video_data})


def create_video_for_gallery(request):
    if request.method == 'POST':
        form = VideoGalleryForm(request.POST, request.FILES)
        if form.is_valid(): 
            video_link = form.cleaned_data.get('video_link')
            video_id=extract_video_id(video_link)

            if not video_id:
                messages.warning(request, "Enter only embeded code")
                return redirect('/admin/video_gallery_list')
            form.save()
            messages.success(request, "Video Added Successfully")
        else:
            messages.error(request, "Error Adding Video")
        return redirect('/admin/video_gallery_list')
    else:
        messages.warning(request, "Only POST method is allowed for this operation.")
        return redirect('/admin/video_gallery_list')
 

def delete_video_from_gallery(request,id):
    VideoGallery.objects.get(id=id).delete()
    return redirect("/admin/video_gallery_list")





@login_required
def enquiry_list(request):
    enquiries = Enquiry.objects.order_by('-id')
    return render(request, 'enquiry_list.html', {'enquiries': enquiries})

def delete_enquiry(request,id):
    Enquiry.objects.get(id=id).delete()
    return redirect("/admin/enquiry_list")
 





from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Product, ProductMedia
from .forms import ProductForm, ProductMediaForm
from django.forms import modelformset_factory

# ---------------- Product List ----------------
def product_list(request):
    # try:
        products = Product.objects.all().order_by("-created_at")
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    product = form.save()
                    messages.success(request, "Product created successfully!")
                    return redirect("/admin/product_list")
                except ValidationError as e:
                    return JsonResponse({"success": False, "errors": {"non_field_errors": str(e)}}, status=400)
            else:
                errors = {
                    field: [str(error) for error in error_list]
                    for field, error_list in form.errors.items()
                }
                return JsonResponse({"success": False, "errors": errors}, status=400)
        else:
            form = ProductForm()
    
        context = {
            "products": products,
            "form": form,
        }
        return render(request, "admin_product_list.html", context)
    # except Exception as e:
    #     return render(request, "404.html", {"error_message": str(e)})


 

# ---------------- Update Product ----------------
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_detail", pk=product.id)
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            messages.error(request, f"Product Not Updated. {errors}")
    else:
        form = ProductForm(instance=product)
    return render(request, "admin_update_product.html", {"form": form, "product": product})


# ---------------- Delete Product ----------------
def delete_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        product.delete()
        messages.success(request, "Product deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Product: {str(e)}")
    return redirect("/admin/product_list")


# ---------------- Product Detail ----------------
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    specifications = product.specifications.all().order_by("order")
    media = product.media.all().order_by("order")

    context = {
        "product": product,
        "specifications": specifications,
        "media": media,
    }
    return render(request, "products/product_detail.html", context)
