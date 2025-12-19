from openpyxl import Workbook
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .models import LeaveRequest
from attendance.models import Attendance


# =========================
# STAFF: APPLY LEAVE
# =========================
@login_required
@require_POST
def apply_leave(request):
    user = request.user

    leave_type = request.POST.get("leave_type")
    reason = request.POST.get("reason")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    if not all([leave_type, reason, start_date, end_date]):
        return HttpResponse("All fields are required", status=400)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    today = timezone.now().date()

    if start_date > end_date:
        return HttpResponse("Start date cannot be after end date", status=400)

    if start_date < today:
        return HttpResponse("Cannot apply leave for past dates", status=400)

    overlapping_leave = LeaveRequest.objects.filter(
        user=user,
        status="APPROVED",
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists()

    if overlapping_leave:
        return HttpResponse(
            "You already have an approved leave in this period",
            status=400
        )

    LeaveRequest.objects.create(
        user=user,
        leave_type=leave_type,
        reason=reason,
        start_date=start_date,
        end_date=end_date,
        status="PENDING"
    )

    return HttpResponse("Leave request submitted successfully")


# =========================
# ADMIN: APPROVE / REJECT LEAVE
# + AUTO-MARK ABSENT
# =========================
@require_POST
def review_leave(request, leave_id):

    # 🔒 admin check
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Login required")

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    action = request.POST.get("action")  # APPROVE or REJECT

    if action not in ["APPROVE", "REJECT"]:
        return HttpResponse("Invalid action", status=400)

    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if leave.status != "PENDING":
        return HttpResponse("Leave already reviewed", status=400)

    # -------- APPROVE --------
    if action == "APPROVE":
        leave.status = "APPROVED"
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()
        leave.save()

        # 🔥 AUTO-MARK ATTENDANCE AS ABSENT
        current_date = leave.start_date
        while current_date <= leave.end_date:
            Attendance.objects.get_or_create(
                user=leave.user,
                date=current_date,
                defaults={"status": "ABSENT"}
            )
            current_date += timedelta(days=1)

        return HttpResponse("Leave approved and attendance marked absent")

    # -------- REJECT --------
    leave.status = "REJECTED"
    leave.reviewed_by = request.user
    leave.reviewed_at = timezone.now()
    leave.save()

    return HttpResponse("Leave rejected successfully")


# =========================
# STAFF: VIEW OWN LEAVE HISTORY
# =========================
@login_required
def staff_leave_history(request):
    leaves = LeaveRequest.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    if not leaves.exists():
        return HttpResponse("No leave records found")

    response = []
    for leave in leaves:
        response.append(
            f"""
Leave ID: {leave.id}
Type: {leave.leave_type}
From: {leave.start_date}
To: {leave.end_date}
Status: {leave.status}
Applied At: {leave.applied_at}
-------------------------
"""
        )

    return HttpResponse("".join(response), content_type="text/plain")


# =========================
# ADMIN: VIEW ALL LEAVE HISTORY
# =========================
@login_required
def admin_leave_history(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    leaves = LeaveRequest.objects.all().order_by("-applied_at")

    if not leaves.exists():
        return HttpResponse("No leave records found")

    response = []
    for leave in leaves:
        response.append(
            f"""
Leave ID: {leave.id}
Staff: {leave.user.username}
Type: {leave.leave_type}
From: {leave.start_date}
To: {leave.end_date}
Status: {leave.status}
Reviewed By: {leave.reviewed_by}
Reviewed At: {leave.reviewed_at}
-------------------------
"""
        )

    return HttpResponse("".join(response), content_type="text/plain")
@login_required
def export_my_leaves_excel(request):
    leaves = LeaveRequest.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    wb = Workbook()
    ws = wb.active
    ws.title = "My Leave History"

    ws.append([
        "Leave ID",
        "Leave Type",
        "Start Date",
        "End Date",
        "Status",
        "Applied At",
    ])

    for leave in leaves:
        ws.append([
            leave.id,
            leave.leave_type,
            leave.start_date.strftime("%Y-%m-%d"),
            leave.end_date.strftime("%Y-%m-%d"),
            leave.status,
            leave.applied_at.strftime("%Y-%m-%d"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="my_leaves.xlsx"'
    )

    wb.save(response)
    return response
@login_required
def export_all_leaves_excel(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    leaves = LeaveRequest.objects.all().order_by("-applied_at")

    wb = Workbook()
    ws = wb.active
    ws.title = "All Leave History"

    ws.append([
        "Leave ID",
        "Staff",
        "Leave Type",
        "Start Date",
        "End Date",
        "Status",
        "Reviewed By",
        "Reviewed At",
    ])

    for leave in leaves:
        ws.append([
            leave.id,
            leave.user.username,
            leave.leave_type,
            leave.start_date.strftime("%Y-%m-%d"),
            leave.end_date.strftime("%Y-%m-%d"),
            leave.status,
            leave.reviewed_by.username if leave.reviewed_by else "",
            leave.reviewed_at.strftime("%Y-%m-%d") if leave.reviewed_at else "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="all_leaves.xlsx"'
    )

    wb.save(response)
    return response
@login_required
def admin_leave_statistics(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    total = LeaveRequest.objects.count()
    pending = LeaveRequest.objects.filter(status="PENDING").count()
    approved = LeaveRequest.objects.filter(status="APPROVED").count()
    rejected = LeaveRequest.objects.filter(status="REJECTED").count()

    casual = LeaveRequest.objects.filter(leave_type="CASUAL").count()
    sick = LeaveRequest.objects.filter(leave_type="SICK").count()
    emergency = LeaveRequest.objects.filter(leave_type="EMERGENCY").count()

    return HttpResponse(
        f"""
LEAVE STATISTICS (ADMIN)
-----------------------
Total Requests : {total}
Pending        : {pending}
Approved       : {approved}
Rejected       : {rejected}

Leave Type Breakdown:
Casual         : {casual}
Sick           : {sick}
Emergency      : {emergency}
""",
        content_type="text/plain"
    )
@login_required
def staff_leave_statistics(request):
    user = request.user

    total = LeaveRequest.objects.filter(user=user).count()
    pending = LeaveRequest.objects.filter(user=user, status="PENDING").count()
    approved = LeaveRequest.objects.filter(user=user, status="APPROVED").count()
    rejected = LeaveRequest.objects.filter(user=user, status="REJECTED").count()

    return HttpResponse(
        f"""
MY LEAVE STATISTICS
------------------
Total Requests : {total}
Pending        : {pending}
Approved       : {approved}
Rejected       : {rejected}
""",
        content_type="text/plain"
    )
