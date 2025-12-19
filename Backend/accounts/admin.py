from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import StaffProfile


# =========================
# INLINE STAFF PROFILE
# =========================
class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    extra = 0
    verbose_name_plural = "Staff Profile"


# =========================
# CUSTOM USER ADMIN
# =========================
class CustomUserAdmin(BaseUserAdmin):
    inlines = (StaffProfileInline,)

    # Custom column for staff role
    def staff_role(self, obj):
        if obj.is_superuser:
            return "Admin"
        if hasattr(obj, "staffprofile"):
            return obj.staffprofile.staff_category
        return "No Role"

    staff_role.short_description = "Staff Role"

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "staff_role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "staffprofile__mobile_number",
    )


# =========================
# REGISTER USER ADMIN
# =========================
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
