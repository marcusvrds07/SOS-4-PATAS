from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('voluntario/', views.voluntario, name='voluntario'),
    path('animal/<int:id>/', views.animal_detail, name='animal_detail'),
]
