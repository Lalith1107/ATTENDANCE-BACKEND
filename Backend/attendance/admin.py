from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    # What admin sees in list view
    list_display = (
        'user',
        'date',
        'check_in_time',
        'check_out_time',
        'status',
        'admin_override',
    )

    # Filters on right side
    list_filter = (
        'status',
        'admin_override',
        'date',
    )

    # Search by username
    search_fields = ('user__username',)

    # Default ordering
    ordering = ('-date',)

    # Protect identity fields
    readonly_fields = (
        'user',
        'date',
    )

    # Clean layout inside edit page
    fieldsets = (
        ('User & Date (Locked)', {
            'fields': (
                'user',
                'date',
            )
        }),
        ('Attendance Status', {
            'fields': (
                'status',
                'admin_override',
                'auto_checked_out',
            )
        }),
        ('Time Override (Admin Only)', {
            'fields': (
                'check_in_time',
                'check_out_time',
            )
        }),
    )
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
