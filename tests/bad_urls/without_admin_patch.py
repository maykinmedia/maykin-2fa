from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from maykin_2fa.urls import urlpatterns, webauthn_urlpatterns

urlpatterns = [
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path("admin/", include((urlpatterns, "maykin_2fa"))),
    path("admin/", include((webauthn_urlpatterns, "two_factor"))),
    path("admin/", admin.site.urls),
]
