from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from django.utils.timezone import make_naive
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from webapp.forms import TasksForm
from webapp.models import Tasks, Projects



class TasksView(TemplateView):
    template_name = 'tasks/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['Tasks'] = task
        return context

class TasksCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TasksForm
    model = Tasks

    def form_valid(self, form):
        project = get_object_or_404(Projects, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)

class TasksUpdateView(LoginRequiredMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/task_update.html'
    form_class = TasksForm

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.object.pk})


class TasksDeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/tasks_delete.html'
    success_url = reverse_lazy('index')



