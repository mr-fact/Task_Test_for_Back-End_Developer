from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from taski.project.views import ProjectViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='projects')

urlpatterns = [

] + router.urls
