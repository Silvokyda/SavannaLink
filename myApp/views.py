from django.shortcuts import render
from .models import Livestock  
from .forms import ContactSellerForm 

def livestock_list(request):
    livestock_list = Livestock.objects.all() 
    return render(request, 'livestock/livestock_list.html', {'livestock_list': livestock_list})

def livestock_detail(request, livestock_id):
    try:
        livestock = Livestock.objects.get(id=livestock_id)  
        return render(request, 'livestock/livestock_detail.html', {'livestock': livestock})
    except Livestock.DoesNotExist:
        return render(request, 'livestock/livestock_detail.html', {'livestock': None})

def market_home(request):

    return render(request, 'market/market_home.html', {})

def market_product_detail(request, product_id):

    return render(request, 'market/market_product_detail.html', {'product_id': product_id})


