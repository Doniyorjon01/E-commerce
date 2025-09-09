from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from drf_yasg.generators import OpenAPISchemaGenerator

from accounts.views import CustomTokenObtainPairView, save_image, serve_image

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        try:
            schema = super().get_schema(request, public)
            schema.schemes = ["http", "https"]
            return schema
        except Exception as e:
            print("Swagger schema generation error:", e)
            raise


schema_view = get_schema_view(
    openapi.Info(
        title="TOPGYM-web",
        default_version="v1",
        description="""
TOPGYM — Toshkent shahridagi sport zallarini bir joyda to'plab, foydalanuvchilarga eng qulay tarzda taqdim etadigan onlayn platforma. Sayt orqali siz shahringizdagi turli fitnes markazlari, trenajyor zallari va sport klublari haqida batafsil ma'lumot olishingiz mumkin. Har bir zal sahifasida joylashuvi, narxlari, ish vaqti, xizmat turlari, rasmlar va aloqa ma'lumotlari keltiriladi. Shuningdek, foydalanuvchilar boshqa sport zallari bilan taqqoslash, sharhlarni o'qish va o'z fikrlarini qoldirish imkoniyatiga ega bo'ladilar. TOPGYM sizga sport bilan shug'ullanishni boshlash yoki yangi zal topishni yanada oson va qulay qiladi.

TOPGYM — An online platform that gathers all gyms in Tashkent in one place and presents them in the most convenient way for users. Through the website, you can find detailed information about various fitness centers, gyms, and sports clubs in your city. Each gym page includes location, pricing, working hours, available services, photos, and contact details. Users can also compare different gyms, read reviews, and share their own experiences. TOPGYM makes it easier and more convenient for you to start your fitness journey or find a new place to train.
""",
        contact=openapi.Contact(email="komilov185657@gmail.com"),
        license=openapi.License(name="NOT License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Account
    path('api/v1/profile/', include("accounts.urls")),
    path('api/v1/products/', include("products.urls")),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path("api/v1/image/<str:filename>", serve_image, name="serve_image"),
    path("api/v1/image-save/", save_image, ),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
