from django.urls import path
from sahib.views import scrape_and_search
from django.conf import settings
from django.conf.urls.static import static


app_name = 'scraper'
urlpatterns = [
  path('api/scrape/', scrape_and_search, name='scrape_and_search'),
]