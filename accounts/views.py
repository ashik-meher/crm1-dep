from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory


# Create your views here.


def land(request):
    return render(request, 'land.html', {})


def home(request):
    return render(request, 'home.html', {})


def products(request):

    products = Product.objects.all()

    return render(request, 'products.html', {'products': products})


def customer(request, pk):

    # that makes avaible the dynamic url to this page associated with customer id

    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    orders_count = orders.count()

    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count}

    return render(request, 'customer.html', context)


def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'customer_form.html', context)


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


def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {'item': order}

    return render(request, 'delete.html', context)