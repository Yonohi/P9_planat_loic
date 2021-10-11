from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control",
                                            "value": "{{ticket.title}}"
                                            }),
        }
