from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse

from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView, FormView, CreateView

from webapp.forms import TasksForm
from webapp.models import Tasks


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        data = Tasks.objects.all()

        # http://localhost:8000/?search=ygjkjhg
        search = request.GET.get('search')
        if search:
            data = data.filter(summary__icontains=search)

        return render(request, 'index.html', context={
            'Tasks': data
        })



class TasksView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['Tasks'] = task
        return context

class TasksCreateView(FormView):
    template_name = 'task_create.html'
    form_class = TasksForm

    def form_valid(self, form):
        data = {}
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        task = Tasks.objects.create(**data)
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('task_view', kwargs={'pk': self.Tasks.pk})

class TasksUpdateView(FormView):
    template_name = 'task_update.html'
    form_class = TasksForm

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tasks'] = self.task
        return context

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'type', 'status', 'created_at':
            initial[key] = getattr(self.task, key)
        return initial

    def form_valid(self, form):
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.task, key, value)
        self.task.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tasks, pk=pk)

def task_delete_view(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == 'GET':
        return render(request, 'tasks_delete.html', context={'Tasks': task})
    elif request.method == 'POST':
        Tasks.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
