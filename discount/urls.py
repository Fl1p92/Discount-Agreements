from django.contrib import admin
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.agreement.urls', 'apps.agreement'), namespace='agreement')),
    path('notifications/', include(('apps.notifications.urls', 'apps.notifications'), namespace='notifications')),
    path('api-auth/', include('rest_framework.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
