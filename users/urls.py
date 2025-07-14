from django.urls import path
from .views import CustomLoginView, register, profile, CustomPasswordChangeView, CustomPasswordChangeDoneView, home, custom_logout, users_list, user_create, user_edit, user_detail, user_delete

urlpatterns = [
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('manage-users/', users_list, name='users_list'),
    path('manage-users/add/', user_create, name='user_create'),
    path('manage-users/<int:user_id>/edit/', user_edit, name='user_edit'),
    path('manage-users/<int:user_id>/', user_detail, name='user_detail'),
    path('manage-users/<int:user_id>/delete/', user_delete, name='user_delete'),
] 