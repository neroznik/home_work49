from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse

from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView, FormView

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



class TasksCreateView(View):
    def get(self, request):
        return render(request, 'task_create.html', context={
            'form': TasksForm()
        })

    def post(self, request):
        form = TasksForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            task = Tasks.objects.create(**data)
            return redirect('article_view', pk=task.pk)
        else:
            return render(request, 'task_create.html', context={
                'form': form
            })


class TasksUpdateView(TemplateView):
    template_name = 'task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        initial = {}
        for key in 'summary', 'description', 'type', 'status':
            initial[key] = getattr(task, key)
        form = TasksForm(initial=initial)

        context['Tasks'] = task
        context['form'] = form

        return context

    def post(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        form = TasksForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(task, key, value)
            task.save()
            return redirect('task_view_view', pk=Tasks.pk)
        else:
            return self.render_to_response({
                'Tasks': task,
                'form': form
            })

def task_delete_view(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == 'GET':
        return render(request, 'tasks_delete.html', context={'Tasks': task})
    elif request.method == 'POST':
        Tasks.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
