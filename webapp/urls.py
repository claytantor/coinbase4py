from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'webapp.views.index',name='site_landing'),
    url(r'^index.html$', 'webapp.views.index', name='site_landing_index'),
    url(r'^login.html$', 'webapp.views.login_user', name='login_user'),
    url(r'^home.html$', 'webapp.views.home', name='home'),
    url(r'^logout.html$', 'webapp.views.logout_user', name='logout_user'),


    #coin oauth
    url(r'^coinbase/oauth/$', 'webapp.views.cb_auth_redirect',name='cb_auth_redirect'),

    #coinbase button callback
    url(r'^cbcallback/([\w]+)/$', 'webapp.views.cbcallback',name='cbcallback'),


    #admin
    url(r'^admin/', include(admin.site.urls)),


)

urlpatterns += staticfiles_urlpatterns()
