from django.conf.urls import patterns, url
from kanisa.views.diary import (DiaryRegularEventCreateView,
                                DiaryRegularEventUpdateView,
                                DiaryRegularEventsView,
                                DiaryEventIndexView,
                                DiaryScheduleRegularEventView,
                                DiaryCancelScheduledEventView,
                                DiaryScheduledEventCreateView,
                                DiaryScheduledEventUpdateView,
                                DiaryScheduledEventCloneView,
                                DiaryScheduleWeeksRegularEventView)

urlpatterns = patterns('',
                       url(r'^$',
                           DiaryEventIndexView.as_view(),
                           {},
                           'kanisa_manage_diary'),
                       url(r'^regular/$',
                           DiaryRegularEventsView.as_view(),
                           {},
                           'kanisa_manage_diary_regularevents'),
                       url(r'^regular/create/$',
                           DiaryRegularEventCreateView.as_view(),
                           {},
                           'kanisa_manage_diary_regular_create'),
                       url(r'^regular/edit/(?P<pk>\d+)$',
                           DiaryRegularEventUpdateView.as_view(),
                           {},
                           'kanisa_manage_diary_regular_update'),
                       url(r'^scheduled/create/$',
                           DiaryScheduledEventCreateView.as_view(),
                           {},
                           'kanisa_manage_diary_scheduled_create'),
                       url(r'^scheduled/edit/(?P<pk>\d+)$',
                           DiaryScheduledEventUpdateView.as_view(),
                           {},
                           'kanisa_manage_diary_scheduled_update'),
                       url(r'^schedule/(?P<pk>\d+)/(?P<thedate>\d{8})/$',
                           DiaryScheduleRegularEventView.as_view(),
                           {},
                           'kanisa_manage_diary_schedule_regular_event'),
                       url(r'^schedule/all/$',
                           DiaryScheduleWeeksRegularEventView.as_view(),
                           {},
                           'kanisa_manage_diary_schedule_weeks_regular_event'),
                       url(r'^cancel/(?P<pk>\d+)/$',
                           DiaryCancelScheduledEventView.as_view(),
                           {},
                           'kanisa_manage_diary_cancel_scheduled_event'),
                       url(r'^clone/$',
                           DiaryScheduledEventCloneView.as_view(),
                           {},
                           'kanisa_manage_diary_clone_scheduled_event'),
                       )
