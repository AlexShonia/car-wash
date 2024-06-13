from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.utils import timezone
from .models import Car, Appointment


def indexView(request):
    context = {"logged_in": request.user.is_authenticated}

    return render(request, "car_wash/index.html", context)


def yourAppointments(request):
    if request.POST:
        carModels = request.POST.getlist("model")
        for model in carModels:
            Car.objects.filter(model=model).delete()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        appointments = Appointment.objects.filter(user=request.user)
        print(appointments)
        return render(
            request, "car_wash/your-appointments.html", {"appointments": appointments}
        )


def yourCars(request):
    if request.POST:
        carModels = request.POST.getlist("model")
        for model in carModels:
            Car.objects.filter(model=model).delete()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        cars = Car.objects.filter(user=request.user)
        return render(request, "car_wash/your-cars.html", {"cars": cars})


def appointment(request):
    if request.POST:
        date = request.POST.get("date")
        time = request.POST.get("time")
        model = request.POST.get("car")
        if not date or not time or not model:
            return render(
                request,
                "car_wash/appointment.html",
                {"error_message": "Fill all the fields"},
            )
        car = Car.objects.get(model=model)
        appointment = Appointment(user=request.user, date=(date + " " + time), car=car)
        appointment.save()
        context = {"logged_in": request.user.is_authenticated}
        return render(request, "car_wash/index.html", context)
    else:
        cars = Car.objects.filter(user=request.user)
        print(timezone.now())
        return render(request, "car_wash/appointment.html", {"cars": cars})


def addCar(request):
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
        userName = request.POST.get("username")
        password = request.POST.get("password")
        repeatPassword = request.POST.get("repeatPassword")
        print(email, userName, password, repeatPassword)
        if password != repeatPassword:
            return render(
                request,
                "car_wash/register.html",
                {"error_message": "Passwords don't match"},
            )
        try:
            u = User.objects.get(email=email)
            isUsernameTaken = User.objects.filter(username=userName).exists()
            if isUsernameTaken:
                return render(
                    request,
                    "car_wash/register.html",
                    {"error_message": "This Username is taken"},
                )
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=userName, email=email, password=password
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
