from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse

from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView, FormView, CreateView, ListView

from webapp.forms import TasksForm, SimpleSearchForm
from webapp.models import Tasks

class SearchView(ListView):
    search_form_class = SimpleSearchForm
    search_form_field = 'search'
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value(self.search_form)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        context['search_value'] = self.search_value
        return context

    def get_queryset(self):
        data = super().get_queryset()
        query = self.get_query(self.search_value)
        data = data.filter(query)
        return data

    def get_search_form(self):
        return self.search_form_class(data=self.request.GET)

    def get_search_value(self, form):
        search_value = None
        if form.is_valid():
            search_value = form.cleaned_data.get(self.search_form_field, None)
        return search_value

    def get_query(self, search_value):
        query = Q()
        if search_value:
            for field in self.search_fields:
                kwargs = {field: search_value}
                query = query | Q(**kwargs)
        return query



class IndexView(SearchView):
    template_name = 'index.html'
    context_object_name = 'Tasks'
    paginate_by = 10
    paginate_orphans = 0
    model = Tasks
    ordering = ['-created_at']
    search_fields = ['summary__icontains', 'description__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            return data


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
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})


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
        return {'updated_at': make_naive(self.task.created_at)}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        self.task = form.save()
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
