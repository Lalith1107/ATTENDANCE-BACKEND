from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Attendance


# =========================
# API: CHECK-IN
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_in(request):
    user = request.user
    today = timezone.now().date()

    # Prevent multiple open check-ins
    if Attendance.objects.filter(
        user=user,
        date=today,
        check_out_time__isnull=True
    ).exists():
        return Response(
            {'error': 'Already checked in'},
            status=status.HTTP_400_BAD_REQUEST
        )

    Attendance.objects.create(
        user=user,
        date=today,
        check_in_time=timezone.now(),
        status="PRESENT"
    )

    return Response(
        {'message': 'Checked in successfully'},
        status=status.HTTP_200_OK
    )


# =========================
# API: CHECK-OUT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_out(request):
    attendance = Attendance.objects.filter(
        user=request.user,
        check_out_time__isnull=True
    ).first()

    if not attendance:
        return Response(
            {'error': 'No active session'},
            status=status.HTTP_400_BAD_REQUEST
        )

    attendance.check_out_time = timezone.now()
    attendance.status = "PRESENT"
    attendance.save()

    return Response(
        {'message': 'Checked out successfully'},
        status=status.HTTP_200_OK
    )


# =========================
# API: MY ATTENDANCE LIST
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_attendance(request):
    user = request.user

    attendances = Attendance.objects.filter(
        user=user
    ).order_by('-date')

    data = [
        {
            "date": att.date,
            "check_in_time": att.check_in_time,
            "check_out_time": att.check_out_time,
            "status": att.status,
            "auto_checked_out": att.auto_checked_out,
        }
        for att in attendances
    ]

    return Response({
        "user": user.username,
        "attendance": data
    })
