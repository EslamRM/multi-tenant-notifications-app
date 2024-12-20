from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from auth_jwt.views import (
    TenantAwareTokenObtainPairView,
)
from notifications.views import NotificationViewSet
from search.views import NotificationSearchView

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("search/notifications/", NotificationSearchView.as_view()),
    path(
        "api/token/", TenantAwareTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
]
