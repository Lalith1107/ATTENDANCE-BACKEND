from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

from .models import Attendance


@login_required
def check_in(request):
    user = request.user

    # prevent multiple open check-ins
    if Attendance.objects.filter(user=user, check_out_time__isnull=True).exists():
        return HttpResponse("Already checked in", status=400)

    Attendance.objects.create(
        user=user,
        check_in_time=timezone.now()
    )

    return HttpResponse("Check-in successful")


@login_required
def check_out(request):
    user = request.user

    attendance = Attendance.objects.filter(
        user=user,
        check_out_time__isnull=True
    ).first()

    if not attendance:
        return HttpResponse("No active check-in found", status=400)

    attendance.check_out_time = timezone.now()
    attendance.status = 'PRESENT'
    attendance.save()

    return HttpResponse("Check-out successful")
