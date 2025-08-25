from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from . import serializers
from accounts import models

from django.http import FileResponse, Http404
from django.conf import settings

from rest_framework.decorators import api_view

import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid, base64

from .models import User
from .serializers import RegisterSerializer




from rest_framework.generics import GenericAPIView


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class AccountViewSet(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # ✅ To'g'irlandi: authentication tekshirish keraksiz
        return self.request.user


class AccountUpdateView(generics.UpdateAPIView):
    """
    error: old_and_new_password_id_required_for_change_password, owner_cannot_change_password, old_password_id_wrong
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # ✅ To'g'irlandi: authentication tekshirish keraksiz
        return self.request.user

    def update(self, request, *args, **kwargs):
        new_pass = request.data.get('new_password', None)
        old_pass = request.data.get('old_password', None)

        if (new_pass and not old_pass) or (not new_pass and old_pass):
            return Response({"detail": "old_and_new_password_id_required_for_change_password"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user

        if new_pass and old_pass:
            # ✅ Type check olib tashlandi - hamma user parolini o'zgartirishi mumkin
            if check_password(old_pass, user.password):
                user.set_password(new_pass)
                user.save()
            else:
                return Response({"detail": "old_password_id_wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


@api_view(["GET"])
def serve_image(request, filename):
    # ✅ To'g'irlandi: media/ takrorlanishi
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), content_type="image/*")
    else:
        raise Http404("Image not found")


@api_view(['POST'])
def cleare_data(request, phone_number):
    """Bu function debug uchun, production da o'chirib tashlang"""
    from django.apps import apps
    from accounts.models import User

    for model in apps.get_models():
        for field in model._meta.get_fields():
            if field.is_relation and getattr(field, 'related_model', None) == User:
                print(f"{model.__name__}.{field.name}")

    return Response('success')


class DeleteAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # ✅ Oddiy user delete logic
        user.state = -1
        user.save()
        return Response({"detail": "Account deleted successfully"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def save_image(request):
    try:
        data = request.data
        image_base64 = data.get("image")
        file_type = data.get("file_type", 'png')

        if not image_base64:
            return JsonResponse({"error": "Image is required"}, status=400)

        # ✅ Kengaytirilgan file format support
        allowed_types = ["gif", "png", "jpg", "jpeg", "mp4", "webp"]
        if file_type.lower() not in allowed_types:
            return JsonResponse({"error": f"Invalid file type. Allowed: {', '.join(allowed_types)}"}, status=400)

        image_uuid = str(uuid.uuid4())
        filename = f"{image_uuid}.{file_type}"

        # ✅ To'g'irlandi: folder nomi
        save_path = os.path.join(settings.MEDIA_ROOT, "images/")
        os.makedirs(save_path, exist_ok=True)


        try:
            # ✅ Base64 format tekshirish
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            file_data = base64.b64decode(image_base64)
        except Exception as e:
            return JsonResponse({"error": f"Base64 decoding error: {e}"}, status=400)

        file_path = os.path.join(save_path, filename)

        with open(file_path, "wb") as f:
            f.write(file_data)

        return JsonResponse({
            "message": "File saved successfully",
            "file_name": filename.split('.')[0],
            "full_filename": filename
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
