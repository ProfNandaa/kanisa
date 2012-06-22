from django.db import models
from sorl.thumbnail import ImageField

from kanisa.models.bible.db_field import BiblePassageField


class SermonSeries(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the series.')
    image = ImageField(upload_to='kanisa/sermons/',
                       help_text=u'Must be at least 400px by 300px.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the series '
                                          'cover?'))
    active = models.BooleanField(default=True,
                                 help_text='Is this series currently ongoing?')
    passage = BiblePassageField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def num_sermons(self):
        # This will need implementing once I've got a sermon model - will
        # need to make sure this doesn't result in a query.
        if not hasattr(self, 'fake_num_sermons'):
            import random
            self.fake_num_sermons = random.randint(0, 10)
        return self.fake_num_sermons

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-active', )
        verbose_name_plural = 'Sermon series'


class Sermon(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The title of the sermon.')
    date = models.DateField(help_text='The date the sermon was preached.')
    series = models.ForeignKey(SermonSeries,
                               blank=True, null=True,
                               help_text=('What series the sermon is from, if '
                                          'any.'))
    passage = BiblePassageField(blank=True, null=True)
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the sermon '
                                          'cover?'))

    def __unicode__(self):
        return self.title

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-date', )
