from django.urls import include, path

from testapp.urls import urlpatterns as base_urlpatterns

urlpatterns = [
    *base_urlpatterns,
    path("hijack/", include("hijack.urls")),
]
