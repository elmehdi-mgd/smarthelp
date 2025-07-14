from django.db import models
from django.conf import settings

class Ticket(models.Model):
    URGENCE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
    ]
    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('en_attente', 'En attente'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    urgence = models.CharField(max_length=10, choices=URGENCE_CHOICES, default='moyenne')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouvert')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets_crees', on_delete=models.CASCADE)
    technicien_assigne = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets_assignes', on_delete=models.SET_NULL, null=True, blank=True)
    piece_jointe = models.FileField(upload_to='pieces_jointes/', null=True, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.get_statut_display()})"

class Commentaire(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='commentaires', on_delete=models.CASCADE)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.ticket}"

class HistoriqueTicket(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='historiques', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} par {self.auteur} le {self.date}"
