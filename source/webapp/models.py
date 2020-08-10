from django.utils import timezone
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=10, verbose_name='Статус')

    def __str__(self):
        return "{}".format(self.name, )

class Types(models.Model):
    name = models.CharField(max_length=10, verbose_name='Тип')

    def __str__(self):
        return "{}".format(self.name)


class Tasks(models.Model):
    summary = models.CharField(max_length=100, verbose_name='Задача')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Types', related_name='types', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(verbose_name='Время создания', default=timezone.now)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)



