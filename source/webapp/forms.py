from django import forms
from django.core.exceptions import ValidationError

from .models import Tasks


class TasksForm(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = ['summary', 'description', 'type', 'status']
        widgets = {'type': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        summary = cleaned_data.get('summary')
        description = cleaned_data.get('description')
        if summary and description and summary == description:
            errors.append(ValidationError("Text of the task should not be same with description"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data