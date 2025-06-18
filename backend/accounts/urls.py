from django.urls import path
from .views import SignupView, LoginView, UserRetrieveView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path("user/", UserRetrieveView.as_view(), name="user_retrieve"),
]
