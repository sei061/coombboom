from django.forms import ModelForm, DateTimeInput
from django.forms import ModelForm, CharField, TextInput, DateInput, TimeInput, Textarea, ChoiceField, ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from django import forms

from tasks.models import Task
from .models import Entry


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'


class AddEntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['comment', 'place', 'start_date', 'end_date', 'from_time', 'end_time', 'task']
        labels = {
            'comment': _(''),
            'place': _(''),
            'task': _('Velg oppgave '),

        }

        widgets = {
            'comment': Textarea(attrs={'class': 'form-control form-control-user bg-gradient-dark-highlight',
                                       'placeholder': 'Kommentar', 'rows': 1}),
            'place': TextInput(attrs={'class': 'form-control form-control-user bg-gradient-dark-highlight',
                                      'placeholder': 'Sted'}),
            'start_date': DateInput(),
            'end_date': DateInput(),
            'from_time': TimeInput(),
            'end_time': TimeInput()

        }
