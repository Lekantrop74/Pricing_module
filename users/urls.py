from users.views import UsersListView, UsersDetailView, UsersUpdateView, UsersDeleteView, UsersRegistrationView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


app_name = "users"


urlpatterns = [
    path("show/", UsersListView.as_view(), name='show'),
    path("detail/<int:pk>/", UsersDetailView.as_view(), name='detail'),
    path("update/<int:pk>/", UsersUpdateView.as_view(), name='update'),
    path("delete/<int:pk>/", UsersDeleteView.as_view(), name='delete'),
    path("registration/", UsersRegistrationView.as_view(), name='registration'),
    path('token/', TokenObtainPairView.as_view(), name="take_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),
]
