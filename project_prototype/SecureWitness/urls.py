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
    url(r'^userportal/(?P<curr_user>\w+)/$', views.user_portal, name = 'userportal'), #unique user pages used for group request validation
    url(r'^settings/', views.user_settings, name = 'settings'),
    url(r'^group/(?P<usergroup>\w+)/$', views.group, name='group'),
    url(r'^group/(?P<usergroup>\w+)/request/$', views.request_access, name='request'), #currently editting
    url(r'^report/(?P<selectedReport>\w+)/$', views.report, name='report'),
    url(r'^FileUpload/(?P<reportTitle>\w+)/$', views.FileUpload, name='FileUpload'),
    url(r'^edit/(?P<reportTitle>\w+)/$', views.editReport, name='edit'),
    url(r'^delete/(?P<reportTitle>\w+)/$', views.deleteReport, name='delete')
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #puts in proper folder
