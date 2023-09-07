from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(cls, attrs):
        data = super(UserTokenObtainPairSerializer, cls).validate(attrs)

        refresh = cls.get_token(cls.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if cls.user.is_superuser:
            data["role"] = "superuser"
        else:
            data["role"] = "user"

        return data
