from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/<int:livestock_id>/', views.livestock_detail, name='livestock_detail'),
    path('market/', views.market_home, name='market_home'),
    path('market/product/<int:product_id>/', views.market_product_detail, name='market_product_detail'),
]
