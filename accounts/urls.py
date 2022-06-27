from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/", views.product, name="product"),
    path("customer/<str:pk_test>/", views.customer, name="customer"),
    path("user/", views.userPage, name="user-page"),
    path("create_order/<str:pk>/", views.createOrder, name="create_order"),
    path("update_order/<str:pk>/", views.updateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.deleteOrder, name="delete_order"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("account/", views.account_settings, name="account"),
]
