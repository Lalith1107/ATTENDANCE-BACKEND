from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Attendance

# 🔴 Location logic TEMPORARILY DISABLED
# from locations.models import Geofence
# from locations.utils import calculate_distance
# from locations.models import LocationLog


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_in(request):
    user = request.user

    # Prevent multiple open check-ins
    if Attendance.objects.filter(
        user=user,
        check_out_time__isnull=True
    ).exists():
        return Response(
            {'error': 'Already checked in'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Create attendance without location validation
    Attendance.objects.create(
        user=user,
        check_in_time=timezone.now(),
        status="PRESENT"
    )

    return Response(
        {'message': 'Checked in successfully (location disabled)'},
        status=status.HTTP_200_OK
    )


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
