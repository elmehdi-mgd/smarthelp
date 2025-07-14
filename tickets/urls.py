from django.urls import path
from .views import tickets_list, ticket_create, ticket_detail, ticket_edit, ticket_delete

urlpatterns = [
    path('', tickets_list, name='tickets_list'),
    path('create/', ticket_create, name='ticket_create'),
    path('<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('<int:ticket_id>/edit/', ticket_edit, name='ticket_edit'),
    path('<int:ticket_id>/delete/', ticket_delete, name='ticket_delete'),
] 