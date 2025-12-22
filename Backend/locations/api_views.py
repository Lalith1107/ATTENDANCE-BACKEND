from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
<<<<<<< HEAD
=======
from django.utils import timezone
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d

from .models import Geofence, LocationLog
from .utils import is_inside_geofence


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_ping(request):
<<<<<<< HEAD
=======
    """
    Staff sends location ping every 30 minutes
    Used for attendance validation
    """

>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')

    if lat is None or lon is None:
        return Response(
<<<<<<< HEAD
            {'error': 'Location data missing'},
            status=status.HTTP_400_BAD_REQUEST
        )

    geofence = Geofence.objects.first()  # single campus assumption
=======
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
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d

    inside = False
    if geofence:
        inside = is_inside_geofence(
<<<<<<< HEAD
            float(lat),
            float(lon),
=======
            lat,
            lon,
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
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

<<<<<<< HEAD
    return Response({
        'inside_geofence': inside
    })
=======
    return Response(
        {
            'message': 'Location ping recorded',
            'inside_geofence': inside,
            'timestamp': timezone.now()
        },
        status=status.HTTP_200_OK
    )
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
