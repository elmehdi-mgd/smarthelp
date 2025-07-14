from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout, get_user_model
from django import forms

# Create your views here.

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            messages.success(request, "Compte créé avec succès. Connectez-vous !")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and email != request.user.email:
            request.user.email = email
            request.user.save()
    return render(request, 'profile.html', {'user': request.user})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = '/password_change/done/'

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('dashboard_admin')
        elif request.user.role == 'technicien':
            return redirect('dashboard_technicien')
        else:
            return redirect('dashboard_user')
    return redirect('login')

def custom_logout(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def users_list(request):
    users = User.objects.exclude(role='admin')
    return render(request, 'users/users_list.html', {'users': users})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password('azer1234')
            user.save()
            return redirect('users:users_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Ajouter'})

@user_passes_test(is_admin)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role == 'admin':
        return redirect('users:users_list')
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:users_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Modifier'})

@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role == 'admin':
        return redirect('users:users_list')
    return render(request, 'users/user_detail.html', {'user_obj': user})

@user_passes_test(is_admin)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role == 'admin':
        return redirect('users:users_list')
    if request.method == 'POST':
        user.delete()
        return redirect('users:users_list')
    return render(request, 'users/user_confirm_delete.html', {'user_obj': user})
