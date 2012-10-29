from datetime import timedelta
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent, ScheduledEvent, EventCategory
from kanisa.utils.diary import get_week_bounds, event_covers_date


class DiaryBaseView(object):
    def get_diary_context_data(self, **kwargs):
        return {'events': RegularEvent.objects.all()}


class DiaryIndexView(DiaryBaseView, TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_this_week(self):
        monday, sunday = get_week_bounds()
        events = ScheduledEvent.events_between(monday,
                                               sunday)

        thisweek = []

        for i in range(0, 7):
            thedate = monday + timedelta(days=i)
            thisweek.append((thedate,
                            [e for e in events
                             if event_covers_date(e, thedate)]))

        return thisweek

    def get_category(self, category_key):
        try:
            category = int(category_key)
        except ValueError:
            raise Http404("Bad category value '%s' provided."
                          % category_key)

        if category == 0:
            return None

        try:
            return EventCategory.objects.get(pk=category)
        except EventCategory.DoesNotExist:
            raise Http404("Non-existent category value provided.")

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())
        context['thisweek'] = self.get_this_week()
        context['kanisa_title'] = 'What\'s On'
        categories = EventCategory.objects.filter(num_events__gt=0)
        context['event_categories'] = categories
        category = self.get_category(self.request.GET.get('category', 0))
        context['category'] = category

        if context['category'] is None:
            context['events_to_display'] = context['events']
        else:
            context['events_to_display'] = category.regularevent_set.all()

        return context


class RegularEventDetailView(DiaryBaseView, DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context


class ScheduledEventDetailView(DiaryBaseView, DetailView):
    model = ScheduledEvent
    template_name = 'kanisa/public/diary/scheduledevent.html'

    def get_object(self, queryset=None):
        object = super(ScheduledEventDetailView, self).get_object(queryset)

        if not object.is_special():
            raise Http404("You can't view details for events that aren't "
                          "special.")

        return object

    def get_context_data(self, **kwargs):
        context = super(ScheduledEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context
