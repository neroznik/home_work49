
##Task1

from webapp.models import Tasks, Status
ts1 = Tasks.objects.filter(updated_at__date__gte='2020-08-01') 
ts2 = Tasks.objects.filter(status__name = 'Done')

ts1 & ts2

##Task2
from webapp.models import Tasks, Status, Types

s1 = Tasks.objects.filter(status__name = 'Done')
s2 = Tasks.objects.filter(status__name = 'New ')

s_all = s1|s2

t1 = Tasks.objects.filter(type__name = 'Enhancement')
t2 = Tasks.objects.filter(type__name = 'Bug')

t_all = t1|t2



result = s_all&t_all
result


##Task 3


from webapp.models import Tasks, Status, Types
ts1 = Tasks.objects.filter(summary__icontains='bug')
ts2 = Tasks.objects.filter(type__name = 'Bug')
ts_all = ts1|ts2
result = ts_all.exclude(status__name = 'Done')
result


