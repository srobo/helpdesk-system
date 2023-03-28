from django.urls import path

from .views import HelpdeskDisplayView

app_name = "display"

urlpatterns = [
    path("helpdesk/", HelpdeskDisplayView.as_view(), name="helpdesk"),
]
