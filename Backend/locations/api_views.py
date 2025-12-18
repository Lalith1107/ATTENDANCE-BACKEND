from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Geofence, LocationLog
from .utils import is_inside_geofence


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_ping(request):
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')

    if lat is None or lon is None:
        return Response(
            {'error': 'Location data missing'},
            status=status.HTTP_400_BAD_REQUEST
        )

    geofence = Geofence.objects.first()  # single campus assumption

    inside = False
    if geofence:
        inside = is_inside_geofence(
            float(lat),
            float(lon),
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

    return Response({
        'inside_geofence': inside
    })
