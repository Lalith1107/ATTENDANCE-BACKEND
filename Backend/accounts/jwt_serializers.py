from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import StaffProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_admin'] = user.is_superuser

        if not user.is_superuser:
            try:
                profile = StaffProfile.objects.get(user=user)
                token['staff_category'] = profile.staff_category
            except StaffProfile.DoesNotExist:
                token['staff_category'] = None

        return token
