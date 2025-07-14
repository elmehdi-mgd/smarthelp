from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Commentaire, HistoriqueTicket
from .forms import TicketCreateForm
from users.models import User
from django.core.mail import send_mail

# Create your views here.

@login_required
def tickets_list(request):
    if request.user.role == 'admin':
        tickets = Ticket.objects.all()
    elif request.user.role == 'technicien':
        tickets = Ticket.objects.filter(technicien_assigne=request.user)
    else:
        tickets = Ticket.objects.filter(auteur=request.user)
    return render(request, 'tickets_list.html', {'tickets': tickets})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.auteur = request.user
            ticket.save()
            # Notification email à l'auteur
            send_mail(
                'Ticket créé',
                f'Votre ticket "{ticket.titre}" a bien été créé.',
                None,
                [request.user.email],
            )
            return redirect('tickets_list')
    else:
        form = TicketCreateForm()
    return render(request, 'ticket_create.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    commentaires = Commentaire.objects.filter(ticket=ticket).order_by('date')
    historique = HistoriqueTicket.objects.filter(ticket=ticket).order_by('-date')
    can_edit = request.user == ticket.auteur or request.user.role == 'admin'
    can_delete = request.user == ticket.auteur or request.user.role == 'admin'
    is_admin = request.user.role == 'admin'
    is_technicien = request.user.role == 'technicien' and ticket.technicien_assigne == request.user
    techniciens = User.objects.filter(role='technicien') if is_admin else []
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'assign' and is_admin:
            tech_id = request.POST.get('assign_technicien')
            if tech_id:
                tech = User.objects.filter(id=tech_id, role='technicien').first()
                if tech:
                    ticket.technicien_assigne = tech
                    ticket.save()
                    HistoriqueTicket.objects.create(ticket=ticket, action=f"Assigné à {tech.username}", auteur=request.user)
                    # Notification email au technicien
                    if tech.email:
                        send_mail(
                            'Nouveau ticket assigné',
                            f'Un ticket vous a été assigné : "{ticket.titre}".',
                            None,
                            [tech.email],
                        )
                    return redirect('ticket_detail', ticket_id=ticket.id)
        elif action == 'statut' and is_technicien:
            statut = request.POST.get('statut')
            if statut in dict(ticket.STATUT_CHOICES):
                ticket.statut = statut
                ticket.save()
                HistoriqueTicket.objects.create(ticket=ticket, action=f"Statut changé en {ticket.get_statut_display()}", auteur=request.user)
                # Notification email à l'auteur si résolu
                if statut == 'resolu' and ticket.auteur.email:
                    send_mail(
                        'Ticket résolu',
                        f'Votre ticket "{ticket.titre}" a été résolu.',
                        None,
                        [ticket.auteur.email],
                    )
                return redirect('ticket_detail', ticket_id=ticket.id)
        else:
            texte = request.POST.get('texte')
            if texte:
                Commentaire.objects.create(ticket=ticket, auteur=request.user, texte=texte)
                HistoriqueTicket.objects.create(ticket=ticket, action="Ajout d'un commentaire", auteur=request.user)
                return redirect('ticket_detail', ticket_id=ticket.id)
    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'commentaires': commentaires,
        'historique': historique,
        'can_edit': can_edit,
        'can_delete': can_delete,
        'is_admin': is_admin,
        'is_technicien': is_technicien,
        'techniciens': techniciens,
    })

@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not (request.user == ticket.auteur or request.user.role == 'admin'):
        return redirect('ticket_detail', ticket_id=ticket.id)
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            HistoriqueTicket.objects.create(ticket=ticket, action="Modification du ticket", auteur=request.user)
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketCreateForm(instance=ticket)
    return render(request, 'ticket_edit.html', {'form': form, 'ticket': ticket})

@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not (request.user == ticket.auteur or request.user.role == 'admin'):
        return redirect('ticket_detail', ticket_id=ticket.id)
    if request.method == 'POST':
        HistoriqueTicket.objects.create(ticket=ticket, action="Suppression du ticket", auteur=request.user)
        ticket.delete()
        return redirect('tickets_list')
    return render(request, 'ticket_confirm_delete.html', {'ticket': ticket})
