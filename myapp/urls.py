from django.urls import path
from . import views
from .views import TransView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('createtransaction', views.create_transaction, name='createtransaction'),
    path('download/<str:id>', views.download_receipt, name='download_receipt'),
    
    
    path('api/transaction', TransView.as_view(), name='transaction'),
    path('api/token', obtain_auth_token, name='gettoken'),
    
]