from django import forms

from .models import EnvironmentVariable


class EnvironmentVariableForm(forms.ModelForm):
    class Meta:
        model = EnvironmentVariable
        fields = ('project', 'key', 'value', 'is_secret')
        widgets = {
            'value': forms.PasswordInput(),
        }
