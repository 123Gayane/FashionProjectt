from django.urls import path
from . import views

urlpatterns = [
    path('fashion/', views.fashion_list, name='fashion-list'),
    path('fashion/<int:pk>/', views.fashion_detail, name='fashion-detail'),


    path('contact/', views.contact_list, name='contact-list'),
    path('contact/<int:pk>/', views.contact_detail, name='contact-detail'),


    path('fashion23/', views.fashion2_list, name='fashion2-list'),
    path('fashion23/<int:pk>/', views.fashion2_detail, name='fashion2-detail'),

    path("api/pay/", views.process_payment, name="process_payment"),

    path('sign_in/', views.signin, name='signinIn'),  # SignIn only admin

]
