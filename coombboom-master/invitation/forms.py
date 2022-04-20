from django import forms

class Invitation(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email