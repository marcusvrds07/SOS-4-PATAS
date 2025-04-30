from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home.urls')),
    path('grappelli/', include('grappelli.urls')),

    path('admin/esqueceu-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('admin/email-enviada/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/senha-redefinida/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)