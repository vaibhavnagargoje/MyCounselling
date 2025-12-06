from django.urls import path,include
from . import views

app_name = 'checkout'

urlpatterns = [
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("remove-coupon/<str:type>/<slug:slug>/", views.remove_coupon, name="remove_coupon"),
    path("<str:type>/<slug:slug>/", views.checkout, name="checkout_view"),
]
	