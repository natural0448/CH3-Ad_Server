from django.urls import path
from . import views

app_name = "media_ads"
urlpatterns = [
    path("decision/", views.decision_view, name="decision"),
    path("events/", views.event_view, name="events"),
    path("context/", views.context_view, name="context"),
]
