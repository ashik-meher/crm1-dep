from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import OrderFilter

# User Creation
from django.contrib.auth.forms import UserCreationForm

# flash message
from django.contrib import messages

# authentication

from django.contrib.auth import authenticate, login, logout

# login restriction

from django.contrib.auth.decorators import login_required

# Create your views here.


def land(request):
    return render(request, 'land.html', {})


def home(request):
    return render(request, 'home.html', {})


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    else:

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Created for ' + user)
                return redirect('login')

        context = {'form': form}

        return render(request, "register.html", context)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    else:

        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('dashboard')

            else:

                messages.info(request, 'Username or Password is incorrect')

    context = {}

    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def products(request):

    products = Product.objects.all()

    return render(request, 'products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk):

    # that makes avaible the dynamic url to this page associated with customer id

    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)

    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count, 'myFilter': myFilter}

    return render(request, 'customer.html', context)


@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'customer_form.html', context)


@login_required(login_url='login')
def updateCustomer(request, pk):

    customer = Customer.objects.get(id=pk)

    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'customer': customer, 'form': form}

    return render(request, 'customer_form.html', context)


def dashboard(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    imp = Order.objects.filter(product__name="S-300")

    total_customers = customers.count()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()

    pending = orders.filter(status='Pending').count()

    context = {'products': products, 'customers': customers, 'orders': orders, 'total_orders': total_orders,
               'total_customers': total_customers, 'delivered': delivered, 'pending': pending, 'imp': imp}

    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=3)

    customer = Customer.objects.get(id=pk)

    # initial={'customer': customer}
    #form = OrderForm(initial={'customer': customer})
    # queryset means ager order thakbe na
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context = {'formset': formset}

    return render(request, 'order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)

    formset = OrderForm(instance=order)

    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context = {'formset': formset}

    return render(request, 'order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {'item': order}

    return render(request, 'delete.html', context)
