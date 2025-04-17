from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('animais/<int:tipo_id>/', views.animal_by_type, name='animal_by_type'),
    path('animal/<int:id>/', views.animal_details, name='animal'),
]
