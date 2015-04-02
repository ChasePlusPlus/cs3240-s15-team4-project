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
    url(r'^portal/', views.user_portal, name = 'portal'),
    url(r'^settings/', views.user_settings, name = 'settings'),
    url(r'^(?P<usergroup>\w+)/$', views.group, name='group'),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #puts in proper folder
