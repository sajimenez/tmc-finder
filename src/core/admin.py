from django.contrib import admin
from .models import Operation


class OperationAdmin(admin.ModelAdmin):
    model = Operation
    list_display = ('code', 'term_min', 'term_max', 'amount_min', 'amount_max', )
    ordering = ('term_min', 'amount_min')


admin.site.register(Operation, OperationAdmin)
