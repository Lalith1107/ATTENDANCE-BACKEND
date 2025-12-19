from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Geofence, LocationLog
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

    # Convert to float
    latitude = float(latitude)
    longitude = float(longitude)

    geofence = Geofence.objects.first()
    if not geofence:
        return Response(
            {'error': 'Geofence not configured'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    distance = calculate_distance(
        latitude,
        longitude,
        geofence.latitude,
        geofence.longitude
    )

    inside_geofence = distance <= geofence.radius_meters

    # Log location
    LocationLog.objects.create(
        user=user,
        latitude=latitude,
        longitude=longitude,
        is_inside_geofence=inside_geofence
    )

    # Optional: link with active attendance (NO violations counter)
    attendance = Attendance.objects.filter(
        user=user,
        check_out_time__isnull=True
    ).first()

    if attendance and (is_mocked or not inside_geofence):
        # future logic: mark flag / auto checkout
        pass

    return Response({
        'inside_geofence': inside_geofence,
        'distance_meters': int(distance)
    })
