from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import StaffProfile

# Inline StaffProfile inside User admin
class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile'

# Custom UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (StaffProfileInline,)

    # Add a custom column to show role/staff category
    def staff_role(self, obj):
        if obj.is_superuser:
            return "Admin"
        elif hasattr(obj, 'staffprofile'):
            return obj.staffprofile.staff_category
        return "No Role"
    
    staff_role.short_description = 'Staff Role'

    # Add the new column to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'staff_role', 'is_active', 'is_staff', 'is_superuser')

# Unregister original User and register custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
