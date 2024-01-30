from django.contrib import admin
from django.urls import include, path

from maykin_2fa.urls import urlpatterns

urlpatterns = [
    path("admin/", include((urlpatterns, "maykin_2fa"))),
    path("admin/", admin.site.urls),
]
