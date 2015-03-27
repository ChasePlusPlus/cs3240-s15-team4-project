from django.conf.urls import patterns, url
from SecureWitness import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^upload/', views.uploadView, name = 'upload'),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #puts in proper folder
