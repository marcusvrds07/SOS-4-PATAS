"""
URL configuration for sos4patas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from animais.views import add_tipoanimal_ajax, edit_tipoanimal_ajax, delete_tipoanimal_ajax
from painel_admin.views import dashboard_admin, change_password_ajax

urlpatterns = [
    path('', include('home.urls')),

    path('admin/animais/tipoanimal/delete_ajax/', delete_tipoanimal_ajax, name='delete_tipoanimal_ajax'),
    path('admin/animais/tipoanimal/edit_ajax/', edit_tipoanimal_ajax, name='edit_tipoanimal_ajax'),
    path('admin/animais/tipoanimal/add_ajax/', add_tipoanimal_ajax, name='add_tipoanimal_ajax'),
    path('grappelli/', include('grappelli.urls')),

    path('admin/auth/user/<int:user_id>/change_password_ajax/', change_password_ajax, name='change_password_ajax'),
    

    # URLs personalizadas que usam 'admin' mas são independentes do Django Admin
    path('admin/esqueceu-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('admin/email-enviada/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/senha-redefinida/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('admin/', dashboard_admin, name='admin-index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),


]

#config para as imagens funcionar com link
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)