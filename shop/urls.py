from django.urls import path
from .views import bill_detail, billing_page, customer_purchases, purchase_detail

urlpatterns = [
    path("", billing_page, name="billing"),
    path("bill/<int:purchase_id>/", bill_detail, name="bill_detail"),
    path("customer-purchases/", customer_purchases, name="customer_purchases"),
    path("purchase/<int:purchase_id>/", purchase_detail, name="purchase_detail"),
]
