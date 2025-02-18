from django.template import Library, RequestContext

from core.models import NavigationLink

register = Library()


@register.inclusion_tag("tags/navigation.html", takes_context=True)
def navigation(context: RequestContext) -> dict:
    return {**context.flatten(), "links": NavigationLink.objects.all()}
