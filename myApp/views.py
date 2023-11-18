from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Livestock, Cart, UserProfile
from .forms import ProductForm, SignUpForm, ContactSellerForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def landing_page(request):
    return render(request, 'landing_page.html')


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
            return redirect('login')
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

@csrf_exempt
@login_required
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'status': 'success', 'quantity': quantity})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'status': 'success', 'quantity': cart_item.quantity})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_profile_form = UserProfileForm(request.POST or None, instance=user_profile)

    # Product Form
    product_form = ProductForm(request.POST or None)

    # Handle User Profile Form Submission
    if request.method == 'POST' and 'user-info-submit' in request.POST:
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('edit_profile')

    # Handle Product Form Submission
    if request.method == 'POST' and 'product-form' in request.POST:
        if product_form.is_valid():
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

@login_required
def crops_view(request):
    template_name = 'market/category_products.html'
    crops = Product.objects.filter(category='crops')
    return render(request, template_name, {'products': crops})

@login_required
def livestock_view(request):
    template_name = 'market/category_products.html'
    livestock = Product.objects.filter(category='livestock')
    return render(request, template_name, {'products': livestock})

@login_required
def equipment_view(request):
    template_name = 'market/category_products.html'
    equipment = Product.objects.filter(category='tools')
    return render(request, template_name, {'products': equipment})

