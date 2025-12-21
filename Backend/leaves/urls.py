from django.urls import path
from . import views

urlpatterns = [
# path('', views.some_view),

    # =====================
    # STAFF
    # =====================
    path("apply/", views.apply_leave, name="apply_leave"),
    path("my-history/", views.staff_leave_history, name="staff_leave_history"),
    path("stats/my/", views.staff_leave_statistics, name="staff_leave_statistics"),
    path("export/my/", views.export_my_leaves_excel, name="export_my_leaves_excel"),

    # =====================
    # ADMIN
    # =====================
    path(
        "review/<int:leave_id>/",
        views.review_leave,
        name="review_leave"
    ),
    path("all-history/", views.admin_leave_history, name="admin_leave_history"),
    path("stats/admin/", views.admin_leave_statistics, name="admin_leave_statistics"),

    path("export/all/", views.export_all_leaves_excel, name="export_all_leaves_excel")

    path("export/all/", views.export_my_leaves_excel, name="export_my_leaves_excel")

]
