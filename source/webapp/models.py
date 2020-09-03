from django.core.validators import MinLengthValidator, ProhibitNullCharactersValidator
from django.utils import timezone
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=10, verbose_name='Статус')

    def __str__(self):
        return "{}".format(self.name)

class Types(models.Model):
    name = models.CharField(max_length=10, verbose_name='Тип')

    def __str__(self):
        return "{}".format(self.name)

class Projects(models.Model):
    start_time = models.DateTimeField(verbose_name = 'Начало проекта',blank=True)
    end_time = models.DateTimeField(verbose_name='Конец проекта', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Название:', validators=[ProhibitNullCharactersValidator()])
    description = models.TextField(max_length=2000, verbose_name='Описание', validators=[MinLengthValidator(15)])

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


    def __str__(self):
        return "{}. {}".format(self.pk, self.name)



class Tasks(models.Model):
    project = models.ForeignKey('webapp.Projects', related_name='project', on_delete=models.CASCADE, null=True, verbose_name='Проект')
    summary = models.CharField(max_length=100, verbose_name='Задача', validators=[ProhibitNullCharactersValidator()])
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание', validators=[MinLengthValidator(15)])
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ManyToManyField('webapp.Types', related_name='types', blank=True, verbose_name='Тип')
    created_at = models.DateTimeField(verbose_name='Время создания', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='Время обновления', default=timezone.now,  blank=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)



