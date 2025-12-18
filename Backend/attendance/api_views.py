from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Attendance

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_in(request):
    if Attendance.objects.filter(
        user=request.user, check_out_time__isnull=True
    ).exists():
        return Response({'error': 'Already checked in'}, status=400)

    Attendance.objects.create(
        user=request.user,
        check_in_time=timezone.now()
    )
    return Response({'message': 'Checked in'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_out(request):
    attendance = Attendance.objects.filter(
        user=request.user, check_out_time__isnull=True
    ).first()

    if not attendance:
        return Response({'error': 'No active session'}, status=400)

    attendance.check_out_time = timezone.now()
    attendance.save()
    return Response({'message': 'Checked out'})
