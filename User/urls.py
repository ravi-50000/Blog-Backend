from django.urls import path
from User.views import Register, Login, LogOut
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('signin/', Login.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOut.as_view(), name='logout'),
]
