from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import LeaveRequest


VALID_LEAVE_TYPES = ['CASUAL', 'SICK', 'EMERGENCY']
VALID_STATUS = ['APPROVED', 'REJECTED']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave(request):
    data = request.data

    leave_type = data.get('leave_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    reason = data.get('reason')

    if leave_type not in VALID_LEAVE_TYPES:
        return Response(
            {'error': 'Invalid leave type'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not start_date or not end_date:
        return Response(
            {'error': 'Start date and end date are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if start_date > end_date:
        return Response(
            {'error': 'End date cannot be before start date'},
            status=status.HTTP_400_BAD_REQUEST
        )

    LeaveRequest.objects.create(
        user=request.user,
        leave_type=leave_type,
        reason=reason,
        start_date=start_date,
        end_date=end_date
    )

    return Response(
        {'message': 'Leave request submitted'},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(user=request.user).values(
        'id',
        'leave_type',
        'start_date',
        'end_date',
        'status',
        'applied_at'
    )
    return Response(leaves)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_leave_status(request, leave_id):
    if not request.user.is_superuser:
        return Response(
            {'error': 'Unauthorized'},
            status=status.HTTP_403_FORBIDDEN
        )

    status_value = request.data.get('status')

    if status_value not in VALID_STATUS:
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        leave = LeaveRequest.objects.get(id=leave_id)
    except LeaveRequest.DoesNotExist:
        return Response(
            {'error': 'Leave not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Prevent admin approving own leave
    if leave.user == request.user:
        return Response(
            {'error': 'You cannot approve your own leave'},
            status=status.HTTP_400_BAD_REQUEST
        )

    leave.status = status_value
    leave.reviewed_by = request.user
    leave.reviewed_at = timezone.now()
    leave.save()

    return Response({'message': 'Leave status updated'})
