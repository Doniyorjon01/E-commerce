from django.urls import path

from accounts.views import AccountViewSet, AccountUpdateView, RegisterView, DeleteAccountView, \
    CustomTokenObtainPairView

urlpatterns = [
    path('info/', AccountViewSet.as_view(), name='user_info'),
    path('update/', AccountUpdateView.as_view(), name='update_profile'),  # ✅ / qo'shildi
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
]
