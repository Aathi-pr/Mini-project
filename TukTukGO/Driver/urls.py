from django.urls import path

from Driver import views

urlpatterns = [
    path("sign_up_page/", views.sign_up_page, name="sign_up_page"),
    path("driver_process/", views.driver_process, name="driver_process"),
    path("driver_change_pass/", views.driver_change_pass, name="driver_change_pass"),
    path(
        "driver_change_pass_1/", views.driver_change_pass_1, name="driver_change_pass_1"
    ),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback_1/", views.feedback_1, name="feedback_1"),
    path("response_for_tuktuk/", views.response_for_tuktuk, name="response_for_tuktuk"),
    path(
        "response_for_tuktuk_requests/",
        views.response_for_tuktuk_requests,
        name="response_for_tuktuk_requests",
    ),
    path("recept/", views.receipt, name="receipt"),
    path("receipt_requests/", views.receipt_requests, name="receipt_requests"),
    path(
        "receipt_requests_confirm/",
        views.receipt_requests_confirm,
        name="receipt_requests_confirm",
    ),
    path("on_going_ride/", views.on_going_ride, name="on_going_ride"),
    path(
        "on_going_ride_requests/",
        views.on_going_ride_requests,
        name="on_going_ride_requests",
    ),
    path("map_view/", views.map_view, name="map_view"),
    path("driver_ride_details/", views.driver_ride_details, name="driver_ride_details"),
]
