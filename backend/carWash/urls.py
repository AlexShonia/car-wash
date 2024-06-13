from django.urls import path

from . import views

app_name = "carWash"
urlpatterns = [
    path("", views.indexView, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-car", views.addCar, name="addCar"),
    path("appointment", views.appointment, name="appointment"),
]
