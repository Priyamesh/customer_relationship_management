from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory, inlineformset_factory
from accounts import urls
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from accounts.forms import OrderForm
from .models import *
from .filters import *
from .forms import *
from .decorators import *


# Create your views here.


@login_required(login_url="login")
@allowed_user(allowed_roles=["customers"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered_order_count = orders.filter(status="Delivered").count()
    pending_order_count = orders.filter(status="Pending").count()
    print(orders)
    context = {
        "orders": orders,
        "total_order": total_order,
        "delivered_order_count": delivered_order_count,
        "pending_order_count": pending_order_count,
    }
    return render(request, "accounts/user.html", context)


@login_required(login_url="login")
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()

    total_order = orders.count()
    total_customer = customers.count()
    delivered_order_count = orders.filter(status="Delivered").count()
    pending_order_count = orders.filter(status="Pending").count()

    context = {
        "customers": customers,
        "orders": orders,
        "products": products,
        "total_order": total_order,
        "total_customer": total_customer,
        "delivered_order_count": delivered_order_count,
        "pending_order_count": pending_order_count,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@allowed_user(allowed_roles=["admin"])
def product(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {"products": products})


@login_required(login_url="login")
@allowed_user(allowed_roles=["admin"])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    total_orders = customer.order_set.all()
    total_orders_count = total_orders.count()

    myFilter = OrderFilters(request.GET, queryset=total_orders)
    total_orders = myFilter.qs
    # print(total_orders)
    context = {
        "customer": customer,
        "total_orders": total_orders,
        "total_orders_count": total_orders_count,
        "myFilter": myFilter,
    }
    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
@allowed_user(allowed_roles=["admin"])
def createOrder(request, pk):
    OrderFormset = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=5
    )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormset(queryset=Order.objects.none(), instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method == "POST":
        # print('printing request:',request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/customer/" + str(customer.id))

    context = {"formset": formset}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_user(allowed_roles=["customers"])
def account_settings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "accounts/account_settings.html", context)


@login_required(login_url="login")
@allowed_user(allowed_roles=["admin"])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        # print('printing request:',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_user(allowed_roles=["admin"])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {"item": order}

    if request.method == "POST":
        order.delete()
        return redirect("/")

    return render(request, "accounts/delete_order.html", context)


@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "username or password is incorrect")
            return render(request, "accounts/login.html", context)

    return render(request, "accounts/login.html", context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="customers")
            user.groups.add(group)

            Customer.objects.create(user=user)

            messages.success(request, "Profile created for " + username)
            return redirect("/login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("login")
