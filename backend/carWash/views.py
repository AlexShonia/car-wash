from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password


def indexView(request):
    return render(request, "carwash/index.html", {})


def login(request):
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            print("wrong")
            return render(
                request,
                "carwash/login.html",
                {"error_message": "Incorrect Email or Password"},
            )
        else:
            user = authenticate(username=u.username, password=password)
            if user is not None:
                print("suces")
                return render(request, "carwash/index.html", {})
            else:
                return render(
                    request,
                    "carwash/login.html",
                    {"error_message": "Incorrect Email or Password"},
                )
    else:
        return render(request, "carwash/login.html", {})


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
                "carwash/register.html",
                {"error_message": "Passwords don't match"},
            )
        try:
            u = User.objects.get(email=email)
            isUsernameTaken = User.objects.filter(username=userName).exists()
            if isUsernameTaken:
                return render(
                    request,
                    "carwash/register.html",
                    {"error_message": "This Username is taken"},
                )
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=userName, email=email, password=password
            )
            user.save()
            return render(request, "carwash/login.html", {})
        else:
            return render(
                request,
                "carwash/register.html",
                {"error_message": "User with this Email is already registered"},
            )
    else:
        return render(request, "carwash/register.html", {})
