from django.urls import path
from . import views
from django.contrib import admin

app_name = 'user'  # ADD THIS for best practice
urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<str:token>/", views.reset_password, name="reset_password"),
    path("register/", views.register, name="register"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("registration_success/", views.registration_success, name="registration_success"),
    path("login_success/", views.login_success, name="login_success"),


    #after login profile related urls
    path("overview/", views.user_overview, name="overview"),
    path("profile/", views.user_profile, name="user_profile"),
    path("academic_info/", views.academic_info, name="academic_info"),
    path("my_purchases/", views.my_purchases, name="my_purchases"),
    path("settings/", views.account_settings, name="settings"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("change_password/", views.change_password, name="change_password"),
    path("logout/", views.custom_logout, name="custom_logout"),
]