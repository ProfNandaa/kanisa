from django.conf.urls import patterns, url
import kanisa.views.management.users as views


urlpatterns = patterns(
    '',
    url(r'^$', views.user_management, {}, 'kanisa_manage_users'),
    url(r'^activate/(?P<user_id>\d+)/$', views.user_activate, {},
        'kanisa_manage_users_activate'),
    url(r'^spam/(?P<user_id>\d+)/$', views.user_spam, {},
        'kanisa_manage_users_spam'),
    url(r'^create/$', views.user_create, {},
        'kanisa_manage_users_create'),
    url(r'^details/(?P<pk>\d+)/$', views.user_details, {},
        'kanisa_manage_users_details'),
    url(r'^update/(?P<pk>\d+)/$', views.user_update, {},
        'kanisa_manage_users_update'),
)
