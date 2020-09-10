from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

class TasksCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TasksForm
    model = Tasks
    permission_required = 'webapp.add_task'

    def form_valid(self, form):
        project = get_object_or_404(Projects, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

    def has_permission(self):
        article = self.get_object()
        return super().has_permission() or article.author == self.request.user

class TasksUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/task_update.html'
    form_class = TasksForm
    permission_required = 'webapp.change_task'

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() or self.get_object().users == self.request.user

class TasksDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/tasks_delete.html'
    success_url = reverse_lazy('index')
    permission_required = 'webapp.delete_task'

    def has_permission(self):
        return super().has_permission()


