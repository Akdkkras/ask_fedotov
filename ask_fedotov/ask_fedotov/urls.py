from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls"))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]