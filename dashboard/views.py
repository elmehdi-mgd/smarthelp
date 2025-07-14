from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from users.models import User
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@login_required
def dashboard_admin(request):
    if not request.user.role == 'admin':
        return render(request, 'base.html', {'content': "Accès refusé."})
    # Tickets par statut
    statut_labels = [label for _, label in Ticket.STATUT_CHOICES]
    statut_counts = [Ticket.objects.filter(statut=val).count() for val, _ in Ticket.STATUT_CHOICES]
    statut_colors = ['#4f8cff', '#6ee7b7', '#fbbf24', '#10b981', '#6366f1']
    # Tickets par technicien
    techs = User.objects.filter(role='technicien')
    tech_labels = [t.username for t in techs]
    tech_counts = [Ticket.objects.filter(technicien_assigne=t).count() for t in techs]
    tech_colors = ['#4f8cff', '#6ee7b7', '#fbbf24', '#10b981', '#6366f1', '#f43f5e', '#f472b6'][:len(techs)]
    # Taux de résolution
    total = Ticket.objects.count()
    resolus = Ticket.objects.filter(statut='resolu').count()
    fermes = Ticket.objects.filter(statut='ferme').count()
    resolution_labels = ['Résolus', 'Fermés', 'Autres']
    resolution_data = [resolus, fermes, total - resolus - fermes]
    resolution_colors = ['#10b981', '#6366f1', '#fbbf24']
    return render(request, 'dashboard_admin.html', {
        'statut_data': {'labels': statut_labels, 'data': statut_counts, 'colors': statut_colors},
        'tech_data': {'labels': tech_labels, 'data': tech_counts, 'colors': tech_colors},
        'resolution_data': {'labels': resolution_labels, 'data': resolution_data, 'colors': resolution_colors},
    })

@login_required
def dashboard_technicien(request):
    if not request.user.role == 'technicien':
        return render(request, 'base.html', {'content': "Accès refusé."})
    tickets = Ticket.objects.filter(technicien_assigne=request.user)
    # Tickets par statut
    statut_labels = [label for _, label in Ticket.STATUT_CHOICES]
    statut_counts = [tickets.filter(statut=val).count() for val, _ in Ticket.STATUT_CHOICES]
    statut_colors = ['#4f8cff', '#6ee7b7', '#fbbf24', '#10b981', '#6366f1']
    # Tickets par urgence
    urgence_labels = [label for _, label in Ticket.URGENCE_CHOICES]
    urgence_counts = [tickets.filter(urgence=val).count() for val, _ in Ticket.URGENCE_CHOICES]
    urgence_colors = ['#fbbf24', '#4f8cff', '#f43f5e']
    # Evolution sur 7 jours
    today = timezone.now().date()
    labels = [(today - timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
    data = [tickets.filter(date_creation__date=today - timedelta(days=i)).count() for i in range(6, -1, -1)]
    return render(request, 'dashboard_technicien.html', {
        'statut_data': {'labels': statut_labels, 'data': statut_counts, 'colors': statut_colors},
        'urgence_data': {'labels': urgence_labels, 'data': urgence_counts, 'colors': urgence_colors},
        'evolution_data': {'labels': labels, 'data': data},
    })

@login_required
def dashboard_user(request):
    if not request.user.role == 'utilisateur':
        return render(request, 'base.html', {'content': "Accès refusé."})
    tickets = Ticket.objects.filter(auteur=request.user)
    # Tickets par statut
    statut_labels = [label for _, label in Ticket.STATUT_CHOICES]
    statut_counts = [tickets.filter(statut=val).count() for val, _ in Ticket.STATUT_CHOICES]
    statut_colors = ['#4f8cff', '#6ee7b7', '#fbbf24', '#10b981', '#6366f1']
    # Historique sur 6 mois
    today = timezone.now().date()
    labels = []
    data = []
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - timedelta(days=30*i)).strftime('%m/%Y')
        count = tickets.filter(date_creation__month=(today.month-i)%12 or 12, date_creation__year=today.year if today.month-i>0 else today.year-1).count()
        labels.append(month)
        data.append(count)
    return render(request, 'dashboard_user.html', {
        'statut_data': {'labels': statut_labels, 'data': statut_counts, 'colors': statut_colors},
        'history_data': {'labels': labels, 'data': data},
    })

def dashboard_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('dashboard_admin')
        elif request.user.role == 'technicien':
            return redirect('dashboard_technicien')
        else:
            return redirect('dashboard_user')
    return redirect('login')
