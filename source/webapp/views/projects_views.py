from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from webapp.models import Projects
from webapp.forms import ProjectsForm, ProjectUserForm
from .base_views import SearchView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(SearchView):
    template_name = 'projects/index.html'
    context_object_name = 'projects'
    paginate_by = 3
    paginate_orphans = 0
    model = Projects
    ordering = ['name']
    search_fields = ['name__icontains', 'description__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            return data


class ProjectsView(TemplateView):
    template_name = 'projects/project_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        project = get_object_or_404(Projects, pk=pk)

        context['project'] = project
        return context



class ProjectsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    form_class = ProjectsForm
    permission_required = 'webapp.add_projects'

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.project.pk})


class ProjectsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'projects/project_update.html'
    form_class = ProjectsForm
    model = Projects
    permission_required = 'webapp.change_projects'


    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectsUserUpdate (PermissionRequiredMixin, UpdateView):
    template_name = 'projects/project_users.html'
    form_class = ProjectUserForm
    model = Projects
    permission_required = 'webapp.can_change_group'

    def has_permission(self):
        project = self.get_object()
        return super().has_permission() or self.request.user in project.users.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User
        return context


    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'projects/project_delete.html'
    model = Projects
    success_url = reverse_lazy('index')
    permission_required = 'webapp.delete_projects'


