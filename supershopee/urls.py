from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include("manikshop.urls")),
    path('dashboard/', include("admin_dashboard.urls")),
    path('admin/', admin.site.urls),

    ]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)