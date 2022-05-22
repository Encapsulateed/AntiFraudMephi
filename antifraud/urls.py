from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

import antifraud.settings

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls'))
]
if antifraud.settings.DEBUG:
    urlpatterns += static(antifraud.settings.MEDIA_URL, document_root=antifraud.settings.MEDIA_ROOT)
