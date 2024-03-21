from django.contrib import admin
from django.urls import path
from django.urls import include, path


urlpatterns = [
   path("admin/", admin.site.urls),
   path('scraper/', include('sahib.urls')),
]




from django.contrib import admin
from django.urls import path


