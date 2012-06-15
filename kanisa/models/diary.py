from datetime import date, timedelta
from django.db import models


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)


class RegularEvent(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the event.')
    day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK,
                                           help_text=('What day of the week '
                                                      'does this event '
                                                      'happen on?'))
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(default=60,
                                   help_text=u'Duration in minutes.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. Who is this event for? What '
                                          'does it involve? How much does it '
                                          'cost? Where is it held?'))

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('day', 'start_time', )

    def __unicode__(self):
        return self.title

    def schedule(self, start_date, end_date):
        """Schedule an instance of this event, with no custom details
        set up. The instance will be scheduled for all matching dates
        on or after start_date, and before (and not including)
        end_date.
        """
        for single_date in daterange(start_date, end_date):
            if single_date.weekday() != self.day:
                continue

            instance = self.scheduledevent_set.\
                create(date=single_date,
                       start_time=self.start_time,
                       duration=self.duration)


class ScheduledEvent(models.Model):
    event = models.ForeignKey(RegularEvent)
    date = models.DateField()
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(default=60,
                                   help_text=u'Duration in minutes.')
    title = models.CharField(max_length=60, blank=True, null=True,
                             help_text=('If left blank, this defaults to '
                                        'event type.'))
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. Who is this event for? What '
                                          'does it involve? How much does it '
                                          'cost? Where is it held?'))

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('date', 'event__start_time')

    def __unicode__(self):
        if self.title:
            return self.title

        return self.event.title
