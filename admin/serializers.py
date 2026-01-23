from rest_framework import serializers
from accounts.models import User

class UsersSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "profile_image",
            "phone_number",
            "first_name",
            "last_name",
        ]

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None
