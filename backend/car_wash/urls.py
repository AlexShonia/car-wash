from django.urls import path

from . import views

app_name = "car_wash"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-car", views.add_car, name="add_car"),
    path("your-cars", views.your_cars, name="your_cars"),
    path("appointment", views.appointment, name="appointment"),
    path("choose-time", views.choose_time, name="choose_time"),
    path("make-appointment", views.make_appointment, name="make_appointment"),
    path("your-appointments", views.your_appointments, name="your_appointments"),
]
