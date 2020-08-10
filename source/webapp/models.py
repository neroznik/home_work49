from django.utils import timezone
from django.db import models


class Status(models.Model):
    STATUSES =[('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]
    name = models.CharField(max_length=10, choices=STATUSES, default='new')

    def __str__(self):
        return "{}".format(self.name)

class Types(models.Model):
    TYPES = [('task', 'Задача'), ('bug', 'Ошибка'), ('enhancement', 'Улучшение')]
    name = models.CharField(max_length=10, choices=TYPES, default='task')

    def __str__(self):
        return "{}".format(self.name)


class Tasks(models.Model):
    summary = models.CharField(max_length=100, verbose_name='Задача')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, default='new', verbose_name='Статус')
    type = models.ForeignKey('webapp.Types', related_name='types', on_delete=models.PROTECT, default='task', verbose_name='Тип')
    created_at = models.DateTimeField(verbose_name='Время создания', default=timezone.now)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)



