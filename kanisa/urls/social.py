from django.conf.urls import patterns, url
from kanisa.views.social import (SocialIndexView,
                                 SocialTwitterIndexView,
                                 SocialTwitterPostView,
                                 ScheduledTweetCreateView,
                                 ScheduledTweetDeleteView,
                                 ScheduledTweetUpdateView)


urlpatterns = patterns('',
                       url(r'^$',
                           SocialIndexView.as_view(),
                           {},
                           'kanisa_manage_social'),
                       url(r'^twitter/$',
                           SocialTwitterIndexView.as_view(),
                           {},
                           'kanisa_manage_social_twitter'),
                       url(r'^twitter/create/$',
                           ScheduledTweetCreateView.as_view(),
                           {},
                           'kanisa_manage_social_twitter_create'),
                       url(r'^twitter/edit/(?P<pk>\d+)$',
                           ScheduledTweetUpdateView.as_view(),
                           {},
                           'kanisa_manage_social_twitter_update'),
                       url(r'^twitter/delete/(?P<pk>\d+)$',
                           ScheduledTweetDeleteView.as_view(),
                           {},
                           'kanisa_manage_social_twitter_delete'),
                       url(r'^twitter/post/$',
                           SocialTwitterPostView.as_view(),
                           {},
                           'kanisa_manage_social_twitter_post'),
                       )
