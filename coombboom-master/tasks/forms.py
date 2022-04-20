from django.utils.translation import ugettext_lazy as _

from django.forms import Textarea, TextInput, DateTimeInput

from tasks.models import Task
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_name',
            'task_status',
            'est_time',
            'expected_time',
            'start_date']
            #'projects']
        labels = {
            'task_name': _(''),
            'place': _(''),
            'project': _('Velg prosjekt '),
            'task': _('Velg oppgave '),

        }

        widgets = {
            'task_name': Textarea(attrs={'class': 'form-control form-control-user bg-gradient-dark-highlight',
                                         'placeholder': 'Kommentar', 'rows': 1}),
            'place': TextInput(attrs={'class': 'form-control form-control-user bg-gradient-dark-highlight',
                                      'placeholder': 'Sted'}),
            'start_date': DateInput(),
            'expected_time': forms.NumberInput(),
            'est_time': DateInput(),

        }
