from django.urls import path

from User import views

urlpatterns = [
    path(
        "user_process/",
        views.user_process,
        name="user_process",
    ),
    path("user_change_pass/", views.user_change_pass, name="user_change_pass"),  # 16
    path(
        "user_change_pass_1/", views.user_change_pass_1, name="user_change_pass_1"
    ),  # 17
    path("user_feedback/", views.user_feedback, name="user_feedback"),
    path("user_feedback_1/", views.user_feedback_1, name="user_feedback_1"),
    path("user_feedback_reply/", views.user_feedback_reply, name="user_feedback_reply"),
    path(
        "user_feedback_reply_requests/",
        views.user_feedback_reply_requests,
        name="user_feedback_reply_requests",
    ),
    path(
        "user_feedback_details_post/",
        views.user_feedback_details_post,
        name="user_feedback_details_post",
    ),
    path(
        "check_driver_response/",
        views.check_driver_response,
        name="check_driver_response",
    ),
    path(
        "booking_page/",
        views.booking_page,
        name="booking_page",
    ),  # 31
    path(
        "request_tuktuk_and_tuktuk_driver/",
        views.request_tuktuk_and_tuktuk_driver,
        name="request_tuktuk_and_tuktuk_driver",
    ),  # 33
    path(
        "calculate_distance_and_allot_auto/",
        views.calculate_distance_and_allot_auto,
        name="calculate_distance_and_allot_auto",
    ),  # 32
    path("loading/", views.loading, name="loading"),
    path("payment_history/", views.payment_history, name="payment_history"),
    path("feedback_view/", views.feedback_view, name="feedback_view"),
    path(
        "feedback_view_requests/",
        views.feedback_view_requests,
        name="feedback_view_requests",
    ),
    path(
        "ride_details/",
        views.ride_details,
        name="ride_details",
    ),
]
