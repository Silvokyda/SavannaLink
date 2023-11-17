from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Livestock, Cart, UserProfile
from .forms import ProductForm, SignUpForm, ContactSellerForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    products = Product.objects.all()

    # Fetch cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total amount in the cart
    cart_total = cart_items.aggregate(Sum('product__price'))['product__price__sum'] or 0
    
    return render(request, 'market/dashboard.html', {'products': products, 'cart_items': cart_items, 'cart_total': cart_total})

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity')) 
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Product
from .forms import UserProfileForm, ProductForm

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # User Profile Form
    user_profile_form = UserProfileForm(request.POST or None, instance=user_profile)

    # Product Form
    product_form = ProductForm(request.POST or None)

    # Handle User Profile Form Submission
    if request.method == 'POST' and 'user-profile-form' in request.POST:
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('edit_profile')

    # Handle Product Form Submission
    if request.method == 'POST' and 'product-form' in request.POST:
        if product_form.is_valid():
            # Save the product, assuming you have a user field in your Product model
            product = product_form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('edit_profile')

    return render(request, 'market/edit_profile.html', {
        'user_profile_form': user_profile_form,
        'product_form': product_form,
        'user_products': Product.objects.filter(owner=request.user),
    })


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        product.price = new_price
        product.save()

    return redirect('edit_profile')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()

    return redirect('edit_profile')

@csrf_exempt  
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return JsonResponse({'status': 'success', 'message': 'Product added successfully'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ProductForm()

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



