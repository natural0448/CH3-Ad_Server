from django.urls import path

from . import views

app_name = "ads"
urlpatterns = [
    path("advertiser/campaigns/", views.campaign_view, name="campaigns"),
    path("advertiser/bids/", views.bid_view, name="bids"),
    path("advertiser/events/", views.advertiser_event_view, name="web-events"),
    path("api/media/decision/", views.decision_view, name="decision"),
    path("api/media/events/", views.event_view, name="events"),
]
