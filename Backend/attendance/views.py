from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from calendar import monthrange
<<<<<<< HEAD

from django.contrib.auth.models import User
=======
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
from .models import Attendance
from leaves.models import LeaveRequest


# =========================
<<<<<<< HEAD
# STAFF CHECK-IN
=======
# STAFF CHECK-IN (WEB)
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
# =========================
@login_required
@require_POST
def check_in(request):
    user = request.user
    today = timezone.now().date()

<<<<<<< HEAD
    # 🚫 BLOCK CHECK-IN IF APPROVED LEAVE EXISTS
=======
    # 🚫 Block if approved leave exists
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    leave_exists = LeaveRequest.objects.filter(
        user=user,
        status="APPROVED",
        start_date__lte=today,
        end_date__gte=today
    ).exists()

    if leave_exists:
        return HttpResponse(
            "You are on approved leave today. Check-in not allowed.",
            status=403
        )

<<<<<<< HEAD
    # prevent multiple check-ins for the same day
=======
    # Prevent multiple check-ins
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    if Attendance.objects.filter(user=user, date=today).exists():
        return HttpResponse("Already checked in for today", status=400)

    Attendance.objects.create(
        user=user,
        date=today,
        check_in_time=timezone.now(),
        status="PRESENT"
    )

    return HttpResponse("Check-in successful")


# =========================
<<<<<<< HEAD
# STAFF CHECK-OUT
=======
# STAFF CHECK-OUT (WEB)
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
# =========================
@login_required
@require_POST
def check_out(request):
    user = request.user
    today = timezone.now().date()

    try:
        attendance = Attendance.objects.get(
            user=user,
            date=today,
            check_out_time__isnull=True
        )
    except Attendance.DoesNotExist:
        return HttpResponse("No active check-in found for today", status=400)

    if attendance.admin_override:
        return HttpResponse("Attendance locked by admin", status=403)

    attendance.check_out_time = timezone.now()
    attendance.status = "PRESENT"
    attendance.save()

    return HttpResponse("Check-out successful")


# =========================
<<<<<<< HEAD
# STAFF: MONTHLY ATTENDANCE REPORT
=======
# STAFF: MONTHLY REPORT (TEXT)
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
# =========================
@login_required
def staff_monthly_report(request):
    user = request.user

    month = request.GET.get("month")
    year = request.GET.get("year")

    today = timezone.now().date()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    start_date = today.replace(year=year, month=month, day=1)
    end_date = today.replace(
        year=year,
        month=month,
        day=monthrange(year, month)[1]
    )

    records = Attendance.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    )

<<<<<<< HEAD
    total_days = monthrange(year, month)[1]
    present_days = records.filter(status="PRESENT").count()
    absent_days = records.filter(status="ABSENT").count()
    auto_checkout_days = records.filter(status="AUTO_CHECKOUT").count()

=======
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    return HttpResponse(
        f"""
Monthly Attendance Report ({month}/{year})

<<<<<<< HEAD
Total Days       : {total_days}
Present Days     : {present_days}
Absent Days      : {absent_days}
Auto Checkouts   : {auto_checkout_days}
=======
Total Days       : {monthrange(year, month)[1]}
Present Days     : {records.filter(status="PRESENT").count()}
Absent Days      : {records.filter(status="ABSENT").count()}
Auto Checkouts   : {records.filter(status="AUTO_CHECKOUT").count()}
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
""",
        content_type="text/plain"
    )


# =========================
<<<<<<< HEAD
# ADMIN: MONTHLY ATTENDANCE REPORT (ANY STAFF)
# =========================
@login_required
def admin_monthly_report(request, user_id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access only")

=======
# ADMIN: MONTHLY REPORT (TEXT)
# =========================
@login_required
@staff_member_required
def admin_monthly_report(request, user_id):
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    month = request.GET.get("month")
    year = request.GET.get("year")

    today = timezone.now().date()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

<<<<<<< HEAD
=======
    user = User.objects.get(id=user_id)

>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    start_date = today.replace(year=year, month=month, day=1)
    end_date = today.replace(
        year=year,
        month=month,
        day=monthrange(year, month)[1]
    )

<<<<<<< HEAD
    user = User.objects.get(id=user_id)

=======
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    records = Attendance.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    )

<<<<<<< HEAD
    total_days = monthrange(year, month)[1]
    present_days = records.filter(status="PRESENT").count()
    absent_days = records.filter(status="ABSENT").count()
    auto_checkout_days = records.filter(status="AUTO_CHECKOUT").count()

=======
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    return HttpResponse(
        f"""
Monthly Attendance Report for {user.username} ({month}/{year})

<<<<<<< HEAD
Total Days       : {total_days}
Present Days     : {present_days}
Absent Days      : {absent_days}
Auto Checkouts   : {auto_checkout_days}
""",
        content_type="text/plain"
    )
=======
Total Days       : {monthrange(year, month)[1]}
Present Days     : {records.filter(status="PRESENT").count()}
Absent Days      : {records.filter(status="ABSENT").count()}
Auto Checkouts   : {records.filter(status="AUTO_CHECKOUT").count()}
""",
        content_type="text/plain"
    )


# =========================
# STAFF ATTENDANCE LIST (HTML)
# =========================
@login_required
def staff_attendance_view(request):
    attendances = Attendance.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'attendance/staff_attendance_list.html',
        {'attendances': attendances}
    )
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
