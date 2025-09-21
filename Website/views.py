from django.shortcuts import render
from MyAdmin.models import *
# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.conf import settings
import threading

def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation (you can customize this)
        if name and mobile and email and subject and message:
            Enquiry.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request,"Thank You...!") 
            return redirect('/')
        else:
            messages.error(request,"All fields are required")

    return render(request,"index.html")




def send_email_in_background(email_message):
    try:
        email_message.send()
    except Exception as e:
        print(f"Error sending email: {e}")


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and mobile and email and subject and message:
            # Save the enquiry in the database
            Enquiry.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                subject=subject,
                message=message
            )

            # Prepare email content
            email_subject = f"New Enquiry from {name}: {subject}"
            email_body = (
                f"Dear Team,\n\n"
                f"You have received a new enquiry from your website.\n\n"
                f"Details:\n"
                f"Name: {name}\n"
                f"Mobile: {mobile}\n"
                f"Email: {email}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n"
                f"{message}\n\n"
                f"Regards,\n"
                f"Website Enquiry System"
            )

            # Configure the email
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['ims@dynaxcel.com'],  # Replace with the appropriate email address -- sales@dynaxcel.com
            )

            # Send the email in a separate thread to avoid blocking
            email_thread = threading.Thread(target=send_email_in_background, args=(email_message,))
            email_thread.start()

            # Success message to the user
            messages.success(request, "Thank You! Your enquiry has been submitted successfully.")
        else:
            messages.error(request, "All fields are required")

        return redirect('/web/contact-us')

    return render(request, "contact_us.html")



def web_photos_gallary(request):
    categories = PhotoGalleryCategories.objects.prefetch_related('photos').all()
    return render(request, "web_photos_gallary.html", {'categories': categories})

import re

def extract_video_id(embed_url):
    match = re.search(r"embed/([a-zA-Z0-9_-]+)", embed_url)
    if match:
        return match.group(1)
    return None


def web_videos_gallary(request): 
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
  
    return render(request, 'web_video_gallary.html', {"video_data":video_data})




def products(request):
    categories = Category.objects.prefetch_related("products").order_by("name")
    return render(request, "web_products.html", {'categories': categories})



from django.shortcuts import get_object_or_404
def product_details(request, id):
    product_details = get_object_or_404(Product, pk=id)
    
    # Get products from same category (excluding current one)
    related_products = Product.objects.filter(
        category=product_details.category
    ).exclude(id=product_details.id).order_by('-created_at')
    
    return render(
        request,
        "web_product_details.html",
        {"product": product_details, "products": related_products}
    )


def services(request):
    return render(request, "web_services.html")

def faq(request):
    return render(request, "web_faq.html")
 
def about_us(request):
    return render(request, "web_about_us.html")