from django.urls import path
from .views import CustomerRegisterView, CustomerLoginView, CustomerUserView, CustomerLogoutView

urlpatterns = [
    path('customer_register', CustomerRegisterView.as_view()),
    path('customer_login', CustomerLoginView.as_view()),
    path('customer_user', CustomerUserView.as_view()),
    path('customer_logout', CustomerLogoutView.as_view()),
]