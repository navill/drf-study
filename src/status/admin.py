from django.contrib import admin

# Register your models here.
from status.forms import StatusForm
from status.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'image']
    form = StatusForm
    # class Meta:
    #     model = Status


admin.site.register(Status, StatusAdmin)
