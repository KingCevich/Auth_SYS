from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_id"] = self.user.id
        data["email"] = self.user.email
        data["rol"] = self.user.rol

        if hasattr(self.user, "aprobacion_org"):
            data["aprobacion_org"] = self.user.aprobacion_org # opcional

        return data
