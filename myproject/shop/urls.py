from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='About'),
    path('contact/', views.contact, name='Contact'),
    path('tracker/', views.tracker, name='TrackingStatus'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='Checkout'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]