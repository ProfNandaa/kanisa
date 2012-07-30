from django import template
from kanisa.models import Banner, ScheduledTweet


register = template.Library()


@register.simple_tag()
def kanisa_active_banners():
    return Banner.active_objects.count()


@register.simple_tag()
def kanisa_future_scheduled_tweets():
    return ScheduledTweet.future_objects.count()


@register.simple_tag(takes_context=True)
def kanisa_user_has_perm(context, perm):
    user = context['theuser']
    input = '<i class="icon icon-ok"></i>'

    if user.is_superuser:
        return input

    if user.has_perm(perm):
        return input

    return ''
