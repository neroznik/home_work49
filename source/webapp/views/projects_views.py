from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from webapp.models import Projects
from webapp.forms import ProjectsForm
from .base_views import SearchView


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



class ProjectsCreateView(CreateView):
    template_name = 'projects/project_create.html'
    form_class = ProjectsForm

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.project.pk})


class ProjectsUpdateView(UpdateView):
    template_name = 'projects/project_update.html'
    form_class = ProjectsForm
    model = Projects

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})

class ProjectsDeleteView(DeleteView):
    template_name = 'projects/project_delete.html'
    model = Projects
    success_url = reverse_lazy('index')

