import operator

from django.template import Library, RequestContext

from core.models import NavigationLink

register = Library()

# Some links are so universal, it's easier to hardcode them.
STATIC_LINKS = [
    NavigationLink(name="Competition details", url="https://srobo.org/comp"),
    NavigationLink(name="Docs", url="https://srobo.org/docs"),
    NavigationLink(name="Rules", url="https://srobo.org/rules"),
    NavigationLink(name="Runbook", url="https://srobo.org/runbook/"),
]


@register.inclusion_tag("tags/navigation.html", takes_context=True)
def navigation(context: RequestContext) -> dict:
    links = sorted(list(NavigationLink.objects.all()) + STATIC_LINKS, key=operator.attrgetter("name"))
    return {**context.flatten(), "links": links}
