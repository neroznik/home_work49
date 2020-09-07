from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts import forms


class MyUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']


    def clean(self):
        cleaned_data = super().clean()
        errors = []
        if cleaned_data.get('first_name') == '' and cleaned_data.get('last_name') == '':
            errors.append(ValidationError("First or second name name should not be empty"))
            if errors:
                raise ValidationError(errors)
            return cleaned_data



