from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm


# Create your views here.
def index(request):
    return render(request, "user/index.html")


def signin(request):
    page = "login"
    context = {"page": page}
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username not found")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("index")
        else:
            messages.error(request, "Incorrect username or password")
    return render(request, "user/login_register.html", context)


def signup(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["username"]
            user.save()
            messages.success(request, "Account created successfully")
            login(request, user)
            return redirect("index")

    messages.error(request, "Please correct the errors below.")

    context = {"page": page, "form": form}

    return render(request, "user/login_register.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")


def account_view(request):
    user = request.user
    profile = request.user.profile

    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully")
            return redirect('account')

    context = {
        "user": user,
        "profile": profile,
        "form": form,
    }
    return render(request, "user/account.html", context)
