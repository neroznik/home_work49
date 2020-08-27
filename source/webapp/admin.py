from django.contrib import admin

from webapp.models import Tasks, Status, Types, Projects

admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Status)
admin.site.register(Types)
