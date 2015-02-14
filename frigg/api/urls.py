from rest_framework import routers

from .views import BuildViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'builds', BuildViewSet)
