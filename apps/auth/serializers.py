from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.serializers import UserSerializer


class UserTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user"] = UserSerializer(user).data

        return token
