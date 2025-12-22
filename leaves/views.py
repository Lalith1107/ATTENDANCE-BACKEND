from openpyxl import Workbook
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from datetime import datetime, timedelta

from .models import LeaveRequest
from attendance.models import Attendance


# =========================
# STAFF: APPLY LEAVE
# =========================
@login_required
def apply_leave(request):
    if request.method == "GET":
        return render(request, "leaves/apply_leave.html")

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
# =========================
@login_required
def review_leave(request, leave_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    action = request.POST.get("action")
    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if leave.status != "PENDING":
        return HttpResponse("Leave already reviewed", status=400)

    if action == "APPROVE":
        leave.status = "APPROVED"
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()
        leave.save()

        current_date = leave.start_date
        while current_date <= leave.end_date:
            Attendance.objects.get_or_create(
                user=leave.user,
                date=current_date,
                defaults={"status": "ABSENT"}
            )
            current_date += timedelta(days=1)

        return HttpResponse("Leave approved")

    if action == "REJECT":
        leave.status = "REJECTED"
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()
        leave.save()
        return HttpResponse("Leave rejected")

    return HttpResponse("Invalid action", status=400)


# =========================
# STAFF: LEAVE HISTORY (HTML)
# =========================
@login_required
def staff_leave_history(request):
    leaves = LeaveRequest.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    return render(
        request,
        "leaves/my_leave_history.html",
        {"leaves": leaves}
    )


# =========================
# ADMIN: ALL LEAVE HISTORY
# =========================
@login_required
def admin_leave_history(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    leaves = LeaveRequest.objects.all().order_by("-applied_at")

    return render(
        request,
        "leaves/admin_leave_list.html",
        {"leaves": leaves}
    )



# =========================
# STAFF: LEAVE STATISTICS (HTML)
# =========================
@login_required
def staff_leave_statistics(request):
    user = request.user
    context = {
        "total": LeaveRequest.objects.filter(user=user).count(),
        "pending": LeaveRequest.objects.filter(user=user, status="PENDING").count(),
        "approved": LeaveRequest.objects.filter(user=user, status="APPROVED").count(),
        "rejected": LeaveRequest.objects.filter(user=user, status="REJECTED").count(),
    }

    return render(
        request,
        "leaves/staff_leave_stats.html",
        context
    )


# =========================
# ADMIN: LEAVE STATISTICS (HTML)
# =========================
@login_required
def admin_leave_statistics(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

    context = {
        "total": LeaveRequest.objects.count(),
        "pending": LeaveRequest.objects.filter(status="PENDING").count(),
        "approved": LeaveRequest.objects.filter(status="APPROVED").count(),
        "rejected": LeaveRequest.objects.filter(status="REJECTED").count(),
        "casual": LeaveRequest.objects.filter(leave_type="CASUAL").count(),
        "sick": LeaveRequest.objects.filter(leave_type="SICK").count(),
        "emergency": LeaveRequest.objects.filter(leave_type="EMERGENCY").count(),
    }

    return render(
        request,
        "leaves/admin_leave_stats.html",
        context
    )


# =========================
# EXCEL EXPORTS
# =========================
@login_required
def export_my_leaves_excel(request):
    leaves = LeaveRequest.objects.filter(user=request.user)

    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Type", "From", "To", "Status"])

    for leave in leaves:
        ws.append([
            leave.id,
            leave.leave_type,
            leave.start_date,
            leave.end_date,
            leave.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="my_leaves.xlsx"'
    wb.save(response)
    return response
