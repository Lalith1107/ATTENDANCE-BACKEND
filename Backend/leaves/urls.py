from django.urls import path
from .views import (
    apply_leave,
    review_leave,
    staff_leave_history,
    admin_leave_history,
)

urlpatterns = [
    # Staff
    path("apply/", apply_leave, name="apply_leave"),
    path("my-history/", staff_leave_history, name="staff_leave_history"),

    # Admin
    path("review/<int:leave_id>/", review_leave, name="review_leave"),
    path("all-history/", admin_leave_history, name="admin_leave_history"),
]
