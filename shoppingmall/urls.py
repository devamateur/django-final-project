from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToyList.as_view()),
]