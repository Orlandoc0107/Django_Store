from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from accounts import views
from accounts.views import CustomTokenObtainPairView, RegisterClientView, UserGetView, UserPUTView, UserDeleteView
from accounts.views import UserListView, UserDetailsView, AccountsGetView, AccountsPutView, AccountsListView
from accounts.views import AccountsDetailsView, AvatarUploadView, SecurityQuestionView, AnswerVerificationView
from accounts.views import PasswordChangeView, UsernameChangeView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'accounts', views.AccountsViewSet, basename='accounts')


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterClientView.as_view()),
    path('user/', UserGetView.as_view()),
    path('user/edit/', UserPUTView.as_view()),
    path('user/delete/', UserDeleteView.as_view()),
    path('users/list/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailsView.as_view()),
    path('data/', AccountsGetView.as_view()),
    path('data/edit/', AccountsPutView.as_view()),
    path('data/list/', AccountsListView.as_view()),
    path('data/<int:pk>/', AccountsDetailsView.as_view()),
    path('imagen/', AvatarUploadView.as_view()),
    path('security/', SecurityQuestionView.as_view()),
    path('verification/', AnswerVerificationView.as_view()),
    path('password/', PasswordChangeView.as_view()),
    path('username/', UsernameChangeView.as_view()),
]
