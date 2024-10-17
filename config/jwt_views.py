from typing import Dict, Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        response_data = {
            'token': token_data,
            'user': self.user.username,
            'success': True,
        }

        return response_data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
