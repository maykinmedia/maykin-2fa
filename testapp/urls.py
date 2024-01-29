from django.contrib import admin
from django.urls import include, path

from maykin_2fa import monkeypatch_admin

monkeypatch_admin()

urlpatterns = [
    path("admin/", include("maykin_2fa.urls")),
    path("admin/", admin.site.urls),
]
