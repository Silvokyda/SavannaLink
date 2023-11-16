from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/<int:livestock_id>/', views.livestock_detail, name='livestock_detail'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('market/product/<int:product_id>/', views.market_product_detail, name='market_product_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_cart/', views.update_cart, name='update_cart'),
]
