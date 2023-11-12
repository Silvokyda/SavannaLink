from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .models import Product, Livestock
from .forms import ProductForm, SignUpForm, ContactSellerForm
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'landing_page.html')

def livestock_list(request):
    livestock_list = Livestock.objects.all() 
    return render(request, 'livestock/livestock_list.html', {'livestock_list': livestock_list})

def livestock_detail(request, livestock_id):
    try:
        livestock = Livestock.objects.get(id=livestock_id)  
        return render(request, 'livestock/livestock_detail.html', {'livestock': livestock})
    except Livestock.DoesNotExist:
        return render(request, 'livestock/livestock_detail.html', {'livestock': None})

def market_product_detail(request, product_id):

    return render(request, 'market/market_product_detail.html', {'product_id': product_id})

def marketplace(request):
    products = Product.objects.all()
    return render(request, 'market/marketplace.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('marketplace')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def dashboard(request):
    user_products = Product.objects.filter(owner=request.user)
    return render(request, 'market/dashboard.html', {'user_products': user_products})

def logout_view(request):
    logout(request)
    return redirect('landing_page')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'market/add_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('dashboard')

@login_required
def dashboard(request):
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'market/dashboard.html', {'user_products': user_products})
