from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from datetime import datetime
from .models import Car, Appointment


def index_view(request):
    context = {"logged_in": request.user.is_authenticated}
    return render(request, "car_wash/index.html", context)


def your_appointments(request):
    if request.POST:
        dates = request.POST.getlist("date")
        for date_str in dates:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            Appointment.objects.filter(date=date).delete()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        appointments = Appointment.objects.filter(user=request.user)
        print(appointments[0].date)
        return render(
            request, "car_wash/your-appointments.html", {"appointments": appointments}
        )


def your_cars(request):
    if request.POST:
        car_models = request.POST.getlist("model")
        for model in car_models:
            Car.objects.filter(model=model).delete()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        cars = Car.objects.filter(user=request.user)
        return render(request, "car_wash/your-cars.html", {"cars": cars})


def appointment(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, "car_wash/appointment.html", {"cars": cars})


def choose_time(request):
    # current_time = str(timezone.now()).split(" ")[1][:5]

    date = request.POST.get("date")

    request.session["date"] = date
    request.session["car_model"] = request.POST.get("car")

    current_time = "9:00"
    current_hour = int(current_time.split(":")[0])
    current_min = int(current_time.split(":")[1])
    minute_increment = 30

    times = [current_time]

    while current_hour <= 17:
        if int(current_min) == 0:
            current_min = minute_increment
        else:
            current_min = "00"
            current_hour += 1
        current_time = str(current_hour) + ":" + str(current_min)
        if Appointment.objects.filter(date=date + " " + current_time).exists():
            times.append("Reserved")
        else:
            times.append(current_time)

    return render(request, "car_wash/choose_time.html", {"times": times})


def make_appointment(request):
    date = request.session.get("date")
    car_model = request.session.get("car_model")
    time = request.POST.get("time")

    car = Car.objects.get(model=car_model)
    appointment = Appointment(user=request.user, date=(date + " " + time), car=car)
    appointment.save()
    del request.session["date"]
    del request.session["car_model"]

    context = {"logged_in": request.user.is_authenticated}
    return render(request, "car_wash/index.html", context)


def add_car(request):
    if request.POST:
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        type = request.POST.get("type")
        if not brand or not model or not type:
            return render(
                request, "car_wash/car.html", {"error_message": "Fill all the fields"}
            )
        car = Car.objects.create(user=request.user, brand=brand, model=model, type=type)
        car.save()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        return render(request, "car_wash/car.html", {})


def logout_view(request):
    logout(request)
    return render(request, "car_wash/index.html", {})


def login_view(request):
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            print("wrong")
            return render(
                request,
                "car_wash/login.html",
                {"error_message": "Incorrect Email or Password"},
            )
        else:
            user = authenticate(username=u.username, password=password)
            if user is not None:
                login(request, user)
                context = {"logged_in": request.user.is_authenticated}
                return render(request, "car_wash/index.html", context)
            else:
                return render(
                    request,
                    "car_wash/login.html",
                    {"error_message": "Incorrect Email or Password"},
                )
    else:
        return render(request, "car_wash/login.html", {})


def register(request):
    if request.POST:
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeatPassword")
        print(email, username, password, repeat_password)
        if password != repeat_password:
            return render(
                request,
                "car_wash/register.html",
                {"error_message": "Passwords don't match"},
            )
        try:
            u = User.objects.get(email=email)
            is_username_taken = User.objects.filter(username=username).exists()
            if is_username_taken:
                return render(
                    request,
                    "car_wash/register.html",
                    {"error_message": "This Username is taken"},
                )
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            return render(request, "car_wash/login.html", {})
        else:
            return render(
                request,
                "car_wash/register.html",
                {"error_message": "User with this Email is already registered"},
            )
    else:
        return render(request, "car_wash/register.html", {})
