from autoslug import AutoSlugField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    title = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='title', unique=True)
    contents = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children')
    modified = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['slug']

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_pages',
             'Can manage your pages'),
            )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        from haystack import site as haystack_site
        haystack_site.get_index(self.__class__).update_object(self)
