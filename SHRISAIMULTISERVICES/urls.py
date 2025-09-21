"""
URL configuration for DYNAXCEL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Website import views as WebView
from Website import urls as WebUrls
from MyAdmin import urls as WebAdminUrls


from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('default-admin/', admin.site.urls),
    path('', WebView.index, name="index"),
    path('web/', include(WebUrls)),
    path('admin/', include(WebAdminUrls)),
    path('login/', WebAdminUrls.login, name="login"),
    path('logout/', WebAdminUrls.logout, name="logout"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
