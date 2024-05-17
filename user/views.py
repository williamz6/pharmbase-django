from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from backend.models import Drug, OrderItem, Order
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, OrderItemForm


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
        else:
            messages.error(request, "Please correct the errors below.")

    context = {"page": page, "form": form}

    return render(request, "user/login_register.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
def account_view(request):
    user = request.user
    profile = request.user.profile
    orders = OrderItem.objects.filter(orders__customer=profile)

    context = {
        "user": user,
        "profile": profile,
        "orders":orders,
    }
    return render(request, "user/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    user = request.user
    profile = request.user.profile

    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully")
            return redirect("account")

    context = {
        "user": user,
        "profile": profile,
        "form": form,
    }
    return render(request, "user/edit_account.html", context)


@login_required(login_url="login")
def drug(request):
    obj = Drug.objects.all()

    context = {
        "drugs": obj,
    }
    return render(request, "user/drugs.html", context)


@login_required(login_url="login")
def order_item(request, id):
    user = request.user
    profile = request.user.profile

    drug_id = int(id)
    try:
        drug = Drug.objects.get(id=drug_id)
        # if drug.in_stock:
        #     print("Drug in stock")

    except Drug.DoesNotExist:
        return HttpResponseServerError("Drug does not exist")

    if request.method == "POST":
        if drug.in_stock:
            quantity = request.POST.get("quantity")
            price = drug.price_per_item

            try:
                quantity = int(quantity)
            except ValueError:
                return HttpResponseServerError("Invalid quantity")
            
            # calculate total_price
            total_price= quantity * price

            # Create Order instance if it doesn't exist yet
            order, created = Order.objects.get_or_create(customer=profile, total_price=total_price)

            # Create OrderItem directly
            order_item = OrderItem(drug=drug, quantity=quantity, price_per_item=price)
            order_item.save()
            order_item.orders.add(order)
            drug.stock_quantity -= quantity
            drug.save()

            messages.success(request, "Order added")
            return redirect("orders")
        else:
            messages.error(request, "Insufficient stock")

    context = {
        "drug": drug,
        "user": user,
    }
    return render(request, "user/order_drug.html", context)


@login_required(login_url="login")
def orders(request):
    user = request.user
    profile = request.user.profile
    orders = OrderItem.objects.filter(orders__customer=profile)
    context = {"orders": orders}
    return render(request, "user/viewOrders.html", context)
