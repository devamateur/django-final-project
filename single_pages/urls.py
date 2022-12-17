from django.urls import path
from . import views

urlpatterns = [   # IP주소/
    path('', views.landing),
    path('about_us/', views.about_us)  # IP주소/about_us/
]