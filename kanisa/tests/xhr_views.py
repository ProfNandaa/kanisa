from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import AnonymousUser
from datetime import time
from django.test.client import RequestFactory
from kanisa.models import ScheduledEvent, Page, SermonSeries, RegularEvent
from kanisa.tests.utils import KanisaViewTestCase
from kanisa.views.xhr.bible import CheckBiblePassageView
from kanisa.views.xhr.diary import (ScheduleRegularEventView,
                                    DiaryGetSchedule)
from kanisa.views.xhr.pages import CreatePageView, ListPagesView
from kanisa.views.xhr.sermons import MarkSermonSeriesCompleteView
from kanisa.views.xhr.users import AssignPermissionView

import factory


class XHRBaseTestCase(KanisaViewTestCase):
    def setUp(self):
        super(XHRBaseTestCase, self).setUp()
        self.factory = RequestFactory()

    def get_request(self):
        if self.method == 'post':
            request = self.factory.post(self.url)
        else:
            request = self.factory.get(self.url)

        request.session = {}
        request.user = self.fred
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return request

    def fetch_from_factory(self, request, params={}, **kwargs):
        if self.method == 'post':
            request.POST = params
        elif self.method == 'get':
            request.GET = params

        return self.view.as_view()(request, **kwargs)

    def test_xhr_only(self):
        request = self.get_request()
        del request.META['HTTP_X_REQUESTED_WITH']

        resp = self.fetch_from_factory(request)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content,
                         'This page is not directly accessible.')

    def test_correct_method_only(self):
        if self.method == 'get':
            resp = self.client.post(self.url)
        elif self.method == 'post':
            resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.content,
                         '')

    def test_must_be_authenticated(self):
        if not hasattr(self, 'permission_text'):
            return

        request = self.get_request()
        request.user = AnonymousUser()
        resp = self.fetch_from_factory(request)
        self.assertEqual(resp.status_code, 403)


class XHRBiblePassageViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_xhr_biblepassage_check')
    method = 'post'
    view = CheckBiblePassageView

    def test_must_provide_passage(self):
        resp = self.fetch_from_factory(self.get_request(), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'passage' not found.")

    def test_invalid_passage(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'passage': 'Foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         '"Foobar" is not a valid Bible passage.')

    def test_valid_book_invalid_range(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'passage': 'Ps 151'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'There are only 150 chapters in Psalms.')

    def test_valid_passage(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'passage': 'Matt 3v1-7'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Matthew 3:1-7')


class XHRUserPermissionViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_assign_permission')
    method = 'post'
    permission_text = 'manage users'
    view = AssignPermissionView

    def test_must_provide_required_inputs(self):
        # No permission
        resp = self.fetch_from_factory(self.get_request(),
                                       {'user': '3',
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'permission' not found.")

        # No user
        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'foo',
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'user' not found.")

        # No 'assigned'
        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'foo',
                                        'user': '3'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'assigned' not found.")

    def test_input_parsing(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa.manage_users',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can manage your users.')

        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa.manage_users',
                                        'user': 2,
                                        'assigned': 'foobar'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         'fred can no longer manage your users.')

    def test_bad_user(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa.manage_users',
                                        'user': 99,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'No user found with ID 99.')

    def test_bad_permission(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa',
                                        'user': 2,
                                        'assigned': 'true'})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Malformed permission: \'kanisa\'.')

        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa.foo.bar',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Malformed permission: \'kanisa.foo.bar\'.')

        resp = self.fetch_from_factory(self.get_request(),
                                       {'permission': 'kanisa.raspberries',
                                        'user': 2,
                                        'assigned': 'true'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         'Permission \'kanisa.raspberries\' not found.')


class PageFactory(factory.Factory):
    FACTORY_FOR = Page
    title = 'Page Title'


class XHRCreatePageViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_create_page')
    method = 'post'
    permission_text = 'manage pages'
    view = CreatePageView

    def test_must_provide_required_inputs(self):
        # No title
        resp = self.fetch_from_factory(self.get_request(), {'parent': '3', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'title' not found.")

        # No parent
        resp = self.fetch_from_factory(self.get_request(),
                                       {'title': 'Test page', })
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'parent' not found.")

    def test_empty_title(self):
        # Empty title
        resp = self.fetch_from_factory(self.get_request(),
                                       {'title': '', 'parent': ''})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Title must not be empty.')

    def test_nonexistent_parent(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'title': 'Test page', 'parent': '99'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Page with ID \'99\' not found.')

    def test_empty_parent(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'title': 'Test page', 'parent': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Page created.')

    def test_good_parent(self):
        pk = PageFactory.create().pk

        resp = self.fetch_from_factory(self.get_request(),
                                       {'title': 'Test page',
                                        'parent': '%s' % pk})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Page created.')


class XHRListPagesViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_list_pages')
    method = 'get'
    permission_text = 'manage pages'
    view = ListPagesView

    def test_success(self):
        # Make some sample data
        parent = PageFactory.create()
        PageFactory.create(parent=parent)
        PageFactory.create()

        resp = self.fetch_from_factory(self.get_request())
        self.assertEqual(resp.status_code, 200)


class SermonSeriesFactory(factory.Factory):
    FACTORY_FOR = SermonSeries
    title = factory.Sequence(lambda n: 'Series #%s' % n)


class XHRMarkSermonSeriesComplete(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_sermon_series_complete')
    method = 'post'
    permission_text = 'manage sermons'
    view = MarkSermonSeriesCompleteView

    def test_fails_without_required_parameters(self):
        resp = self.fetch_from_factory(self.get_request())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'series' not found.")

    def test_fails_with_non_numeric_series(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'series': 'nonnumeric'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "No sermon series found with ID 'nonnumeric'.")

    def test_fails_with_non_existent_series(self):
        resp = self.fetch_from_factory(self.get_request(), {'series': 99})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "No sermon series found with ID '99'.")

    def test_success(self):
        pk = SermonSeriesFactory.create().pk

        resp = self.fetch_from_factory(self.get_request(), {'series': pk})
        self.assertEqual(resp.status_code, 200)


class RegularEventFactory(factory.Factory):
    FACTORY_FOR = RegularEvent
    title = factory.Sequence(lambda n: 'Regular Event #' + n)
    start_time = time(14, 0)
    duration = 60
    day = 1


class XHRScheduleRegularEventViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_schedule_regular')
    method = 'post'
    permission_text = 'manage the diary'
    view = ScheduleRegularEventView

    def test_required_attributes_are_required(self):
        resp = self.fetch_from_factory(self.get_request(), {'date': 'foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'event' not found.")

        resp = self.fetch_from_factory(self.get_request(), {'event': 'foobar'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         "Required argument 'date' not found.")

    def test_bad_date_format(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'event': 'foobar',
                                        'date': '20121301'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "'20121301' is not a valid date.")

    def test_bad_event_id(self):
        resp = self.fetch_from_factory(self.get_request(),
                                       {'event': '99',
                                        'date': '20121201'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "No event found with ID '99'.")

    def test_success(self):
        pk = RegularEventFactory.create().pk
        resp = self.fetch_from_factory(self.get_request(),
                                       {'event': '%s' % pk,
                                        'date': '20120103'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, "Event scheduled.")

        events = ScheduledEvent.objects.filter(event__pk=1,
                                               date='2012-01-03')
        self.assertEqual(len(events), 1)

    def test_double_schedule(self):
        pk = RegularEventFactory.create().pk
        resp = self.fetch_from_factory(self.get_request(),
                                       {'event': '%s' % pk,
                                        'date': '20120110'})
        self.assertEqual(resp.status_code, 200)

        resp = self.fetch_from_factory(self.get_request(),
                                       {'event': '%s' % pk,
                                        'date': '20120110'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'That event is already scheduled.')


class XHRFetchScheduleViewTest(XHRBaseTestCase):
    url = reverse_lazy('kanisa_manage_xhr_diary_get_schedule',
                       args=['20120101', ])
    method = 'get'
    permission_text = 'manage the diary'
    view = DiaryGetSchedule

    def test_success(self):
        resp = self.fetch_from_factory(self.get_request(), date='20120101')
        self.assertEqual(resp.status_code, 200)

    def test_baddate(self):
        resp = self.fetch_from_factory(self.get_request(), date='2012')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, "Invalid date '2012' provided.")
