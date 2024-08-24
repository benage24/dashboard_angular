from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CustomPermissionViewSet, CustomTokenObtainPairView, ModuleViewSet, RoleCreateView, UserViewSet, \
    UserCreateView

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('module', ModuleViewSet)
router.register('permission', CustomPermissionViewSet)
urlpatterns = [
                  path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('roles/', RoleCreateView.as_view(), name='create-role'),
                  path('create/', UserCreateView.as_view(), name='create-user'),

              ] + router.urls
