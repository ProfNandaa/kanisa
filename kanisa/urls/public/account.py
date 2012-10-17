from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from kanisa.forms.auth import KanisaChangePasswordForm
from kanisa.views import (KanisaRegistrationView,
                          KanisaRegistrationThanksView)
from kanisa.views.public.auth import KanisaLoginView


urlpatterns = patterns('',
                       url(r'^login/$',
                           KanisaLoginView.as_view(),
                           {},
                           'kanisa_public_login'),
                       url(r'^registration/$',
                           KanisaRegistrationView.as_view(),
                           {},
                           'kanisa_public_registration'),
                       url(r'^registration/thanks/$',
                           KanisaRegistrationThanksView.as_view(),
                           {},
                           'kanisa_public_registration_thanks'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'kanisa/logout.html', },
                           'kanisa_public_logout'),
                       url(r'^password/$',
                           password_change,
                           {'template_name': ('kanisa/management/'
                                              'password_reset.html'),
                            'post_change_redirect': '/manage/',
                            'password_change_form': KanisaChangePasswordForm},
                           'kanisa_password_change'),
                       )
