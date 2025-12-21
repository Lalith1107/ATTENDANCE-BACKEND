from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Geofence, LocationLog
from .utils import is_inside_geofence


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_ping(request):
    """
    Staff sends location ping every 30 minutes
    Used for attendance validation
    """

    lat = request.data.get('latitude')
    lon = request.data.get('longitude')

    if lat is None or lon is None:
        return Response(
            {'error': 'Latitude and longitude are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return Response(
            {'error': 'Invalid latitude or longitude'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Assuming single campus / office geofence
    geofence = Geofence.objects.first()

    inside = False
    if geofence:
        inside = is_inside_geofence(
            lat,
            lon,
            geofence.latitude,
            geofence.longitude,
            geofence.radius_meters
        )

    LocationLog.objects.create(
        user=request.user,
        latitude=lat,
        longitude=lon,
        is_inside_geofence=inside
    )

    return Response(
        {
            'message': 'Location ping recorded',
            'inside_geofence': inside,
            'timestamp': timezone.now()
        },
        status=status.HTTP_200_OK
    )
