from django import forms
from django.core.exceptions import ValidationError

from .models import Tasks, Projects


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatepicker_widget.html'

class ProjectsForm(forms.ModelForm):
    start_time = forms.DateTimeField(required=False, label='Начало проекта', input_formats=['%Y-%m-%d'], widget=XDatepickerWidget)
    end_time = forms.DateTimeField(required=False, label='Конец проекта', input_formats=['%Y-%m-%d'], widget=XDatepickerWidget)

    class Meta:
        model = Projects
        fields = ['start_time', 'end_time', 'name', 'description']
        widgets = {'type': forms.CheckboxSelectMultiple}



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


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")