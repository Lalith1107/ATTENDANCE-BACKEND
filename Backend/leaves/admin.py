from django.contrib import admin
<<<<<<< HEAD

# Register your models here.


=======
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'start_date',
        'end_date',
        'status',
    )
    list_filter = ('status',)
    search_fields = ('user__username',)
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
