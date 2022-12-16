from django.urls import path
from . import views

urlpatterns = [   # IP주소/
    path('', views.landing),
]