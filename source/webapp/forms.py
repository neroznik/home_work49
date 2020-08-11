from django import forms

from . import models
from .models import Tasks


class TasksForm(forms.Form):
    summary = forms.CharField(max_length=100, required=True, label='Задача')
    description = forms.CharField(max_length=1000, required=False, label='Описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=models.Status.objects.all(), required=True, widget=forms.Select(attrs={'status':'Статус'}))
    type = forms.ModelChoiceField(queryset=models.Types.objects.all(),required=True, widget=forms.Select(attrs={'type':'Тип'}))
