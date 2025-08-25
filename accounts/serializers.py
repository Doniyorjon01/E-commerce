from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from rest_framework import serializers
from accounts import models
from rest_framework.exceptions import ParseError

from accounts.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = getattr(user, 'email', '')
        token['user_id'] = str(getattr(user, 'id', ''))
        token['fullname'] = getattr(user, 'fullname', '')
        return token



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # ✅ Validation qo'shildi
    # confirm_password = serializers.CharField(write_only=True)  # ✅ Qo'shildi

    class Meta:
        model = models.User
        fields = ('id', 'email', 'password', 'last_name', 'first_name', 'fullname')

    # def validate(self, attrs):
    #     """Password confirmation validation"""
    #     if attrs['password'] != attrs['confirm_password']:
    #         raise serializers.ValidationError("Passwords don't match")
    #     return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class AccountSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'fullname', 'email', 'image_file', 'lang')
        read_only_fields = ('id', 'email')

    def get_image(self, obj):
        """Image URL ni qaytarish"""
        image_file = getattr(obj, 'image_file', None)
        if image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image_file.url)
            return image_file.url
        return None



class AccountUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=255, write_only=True, required=False, min_length=8)
    old_password = serializers.CharField(max_length=255, write_only=True, required=False)
    image = serializers.CharField(required=False, allow_blank=True)  # ✅ Base64 uchun

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'fullname', 'image',
                  'new_password', 'old_password', 'lang', 'fcm_token')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['email'] = instance.email  # ✅ Email qo'shish
        # ✅ Image URL ni to'g'ri qaytarish
        if instance.image_file:
            request = self.context.get('request')
            if request:
                res['image'] = request.build_absolute_uri(instance.image_file.url)
            else:
                res['image'] = instance.image_file.url
        else:
            res['image'] = None
        return res

    def update(self, instance, validated_data):
        # ✅ Password fieldlarini olib tashlash
        validated_data.pop('new_password', None)
        validated_data.pop('old_password', None)

        # ✅ Base64 image processing
        image_data = validated_data.pop('image', None)
        if image_data and image_data.strip():
            try:
                # Base64 prefix ni olib tashlash
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                instance._base64_image_data = image_data
            except Exception as e:
                raise serializers.ValidationError(f"Invalid image format: {e}")

        return super().update(instance, validated_data)