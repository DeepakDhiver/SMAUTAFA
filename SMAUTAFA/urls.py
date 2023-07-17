from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('charts/', views.charts, name='charts'),
    path('news_sentiment/', views.news_sentiment, name='news_sentiment'),
    path('global/', views.global_page, name='global'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('technicals/', views.technicals, name='technicals'),
    path('fundamentals/', views.fundamentals, name='fundamentals'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),