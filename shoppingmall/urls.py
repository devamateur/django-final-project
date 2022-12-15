from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToyList.as_view()),

    path('category/<str:slug>/', views.category_page),  # IP주소/shopping/category/slug/
    path('material/<str:slug>/', views.material_page),  # IP주소/shopping/material/slug/
    path('maker/<int:pk>/', views.maker_page),

]