from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.

def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    products=Product.objects.all()

    total_order=orders.count()
    total_customer=customers.count()
    delivered_order_count=orders.filter(status='Delivered').count()
    pending_order_count=orders.filter(status='Pending').count()

    context={
        'customers':customers,
        'orders':orders,
        'products':products,
        'total_order':total_order,
        'total_customer':total_customer,
        'delivered_order_count':delivered_order_count,
        'pending_order_count':pending_order_count,
    }

    return render(request,'accounts/dashboard.html',context)

def product(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def customer(request):
    return render(request,'accounts/customer.html')
