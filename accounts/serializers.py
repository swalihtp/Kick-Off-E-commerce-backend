from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    is_staff=serializers.ReadOnlyField()
    role=serializers.ReadOnlyField()
    class Meta:
        model=User
        fields=['first_name','last_name','email','password','is_staff','role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        user.is_staff = is_staff
        user.is_active = True if is_staff else False
        user.role='admin' if is_staff else False
        user.save()

        return user

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(email=data['email'],password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user']=user
        return data
    
class ProfileSerializer(serializers.ModelSerializer):
    email=serializers.ReadOnlyField()
    class Meta:
        model=User
        fields=["first_name","last_name","email","profile_image","phone_number"]
    def validate_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must be numeric")
        return value
    
