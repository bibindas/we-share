from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
	url(r'^',include('mess.urls')),
    url(r'^admin/', admin.site.urls),
]

from django.conf import settings


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns