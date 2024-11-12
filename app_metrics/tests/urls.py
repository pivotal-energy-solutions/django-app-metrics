from django.contrib import admin
from django.urls import include

admin.autodiscover()

urlpatterns = [
    (r"^admin/metrics/", include("app_metrics.urls")),
]
