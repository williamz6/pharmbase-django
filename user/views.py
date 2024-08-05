from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from backend.models import Drug, OrderItem, Order
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, OrderForm, OrderItemForm


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
def create_order(request):
    customer = request.user.profile
    if request.method == "POST":
        drug_id = request.POST.get('drug')
        quantity = request.POST.get('quantity')
        quantity = int(quantity)
        drug = Drug.objects.get(id=drug_id)

        order_item_form = OrderItemForm(request.POST)
        if order_item_form.is_valid():
            if drug.stock_quantity >= quantity:
                order = Order.objects.create(customer=customer)
                
                order_item = order_item_form.save(commit=False)
                order_item.order = order
                order_item.drug = drug
                order_item.quantity = quantity
                order_item.save()
            # update stock quantity
                drug.stock_quantity -= order_item.quantity
                drug.save()
                messages.success(request, "ordern has been created")
                return redirect('order-success')
                
            else:
                context={
                    'order_form': order_form,
                    'drugs': Drug.objects.all(),
                    'error': 'Not enough drug in store.'
                }
                return render(request, "user/drugs.html", context)
        else:
            order_form = OrderForm()
            order_item_form = OrderItemForm()
            context={
                    'order_form': order_form,
                    'drugs': Drug.objects.all(),
                    'error': 'Not enough drug in store.'
                }
            return render(request, "user/drugs.html", context)
    return redirect('drugs')
        
@login_required(login_url="login")
def orderSuccess(request):
    return render(request, "user/order_success.html")

""" 
@login_required(login_url="login")

def order_item(request, id):
    drug_id = int(id)
    try:
        drug = Drug.objects.get(id=drug_id)
    except Drug.DoesNotExist:
        return HttpResponseNotFound("Drug not found")

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.profile
            # order.save()
            quantity = request.POST.get('quantity')
            # order.save()
            if OrderItem.is_order_quantity_valid:
                
                OrderItem.objects.create(
                    drugID=drug,
                    orderID=order_item,
                    quantity=int(quantity),
                    unit_price=drug.price_per_item
                )
            else:
                messages.error(request, "Maximum order quantity exceeded")
                return redirect('index')
                
            return redirect("orders")
    else:
        form = OrderItemForm()
    
    context = {
        'drug': drug,
        'form': form,
    }
    return render(request, "user/order_drug.html", context) """

@login_required(login_url="login")
def orders(request):
    user = request.user
    profile = request.user.profile
    orders_list = Order.objects.filter(customer=profile).prefetch_related('items__drug')
    context={
        'orders': orders_list
    }
    return render(request, "user/viewOrders.html", context)
