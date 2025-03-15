from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, logout_user,get_user_list,forgotPassword,verifyOTP

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("logout/", logout_user, name="logout"),
    path("get_user_list/", get_user_list, name="get_user_list"),
    path("forgot_password/", forgotPassword, name="forgot_password"),
    path("reset_password/", verifyOTP, name="verify_otp"),
]