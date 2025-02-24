import operator

from django.template import Library, RequestContext

from core.models import NavigationLink

register = Library()

# Some links are so universal, it's easier to hardcode them.
STATIC_LINKS = [
    NavigationLink("Competition details", "https://srobo.org/comp"),
    NavigationLink("Docs", "https://srobo.org/docs"),
    NavigationLink("Rules", "https://srobo.org/rules"),
    NavigationLink("Runbook", "https://srobo.org/runbook/")
]


@register.inclusion_tag("tags/navigation.html", takes_context=True)
def navigation(context: RequestContext) -> dict:
    links = sorted(list(NavigationLink.objects.all()) + STATIC_LINKS, key=operator.attrgetter("name"))
    return {**context.flatten(), "links": links}
