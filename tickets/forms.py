from django import forms
from .models import Ticket

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titre', 'description', 'urgence', 'piece_jointe'] 