from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('search/', views.search, name='search'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
