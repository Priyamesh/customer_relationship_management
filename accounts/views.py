from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import formset_factory, inlineformset_factory
from accounts import urls
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import OrderForm
from .models import *
from .filters import *


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

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    total_orders=customer.order_set.all()
    total_orders_count=total_orders.count()

    myFilter=OrderFilters(request.GET,queryset=total_orders)
    total_orders=myFilter.qs
    #print(total_orders)
    context={
        'customer':customer,
        'total_orders':total_orders,
        'total_orders_count':total_orders_count,
        'myFilter':myFilter,
    }
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
    OrderFormset=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormset(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method =='POST':
        #print('printing request:',request.POST)
        #form = OrderForm(request.POST)
        formset=OrderFormset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/customer/'+str(customer.id))

    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)

    if request.method =='POST':
        #print('printing request:',request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context={'form':form}
    return render(request,'accounts/order_form.html',context)


def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    context={'item':order}

    if(request.method=="POST"):
        order.delete()
        return redirect('/') 
        

    return render(request,'accounts/delete_order.html',context)

def loginPage(request):
    context={}
    return render(request,'accounts/login.html',context)

def registerPage(request):
    form=UserCreationForm()
    context={'form':form}
    return render(request,'accounts/register.html',context)