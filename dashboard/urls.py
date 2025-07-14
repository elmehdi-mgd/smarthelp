from django.urls import path
from .views import dashboard_admin, dashboard_technicien, dashboard_user, dashboard_redirect

urlpatterns = [
    path('admin/', dashboard_admin, name='dashboard_admin'),
    path('technicien/', dashboard_technicien, name='dashboard_technicien'),
    path('user/', dashboard_user, name='dashboard_user'),
    path('', dashboard_redirect, name='dashboard_redirect'),
] 