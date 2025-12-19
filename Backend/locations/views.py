from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import WorkLocation, LocationLog
from attendance.models import Attendance
from .utils import calculate_distance


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_ping(request):
    user = request.user
    data = request.data

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    is_mocked = data.get('is_mocked', False)

    if latitude is None or longitude is None:
        return Response(
            {'error': 'Latitude and longitude required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    work_location = WorkLocation.objects.first()
    distance = calculate_distance(
        latitude,
        longitude,
        work_location.latitude,
        work_location.longitude
    )

    inside_geofence = distance <= work_location.radius_meters

    LocationLog.objects.create(
        user=user,
        latitude=latitude,
        longitude=longitude,
        is_mocked=is_mocked,
        is_inside_geofence=inside_geofence
    )

    attendance = Attendance.objects.filter(
        user=user,
        check_out_time__isnull=True
    ).first()

    if attendance and (is_mocked or not inside_geofence):
        attendance.location_violations += 1
        attendance.save()

    return Response({
        'inside_geofence': inside_geofence,
        'distance': int(distance)
    })
