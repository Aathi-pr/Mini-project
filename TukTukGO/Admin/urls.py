from django.urls import path

from Admin import views

urlpatterns = [
    path("sign_up_page/", views.sign_up_page, name="sign_up_page"),
    path("admin_process/", views.admin_process, name="admin_process"),
    path("change_pass/", views.change_pass, name="change_pass"),  # 4
    path("change_pass1/", views.change_pass_1, name="change_pass_1"),  # 5
    path(
        "tuktuk_registration/", views.tuktuk_registration, name="tuktuk_registration"
    ),  # 6
    path(
        "tuktuk_registration1/",
        views.tuktuk_registration_1,
        name="tuktuk_registration_1",
    ),  # 7
    path(
        "tuktuk_driver_registration/",
        views.tuktuk_driver_registration,
        name="tuktuk_driver_registration",
    ),  # 8
    path(
        "tuktuk_driver_registration1/",
        views.tuktuk_driver_registration_1,
        name="tuktuk_driver_registration_1",
    ),  # 9
    path("tuktuk_allot/", views.tuktuk_allot, name="tuktuk_allot"),  # 10
    path("tuktuk_allot_1/", views.tuktuk_allot_1, name="tuktuk_allot_1"),  # 11
    path("tuktuk_allot_2/", views.tuktuk_allot_2, name="tuktuk_allot_2"),  # 12
    path("tuktuk_allot_3/", views.tuktuk_allot_3, name="tuktuk_allot_3"),
    path("tuktuk_for_driver/", views.tuktuk_for_driver, name="tuktuk_for_driver"),
    path(
        "tuktuk_for_driver_details/",
        views.tuktuk_for_driver_details,
        name="tuktuk_for_driver_details",
    ),
    path("driver_for_tuktuk/", views.driver_for_tuktuk, name="driver_for_tuktuk"),
    path(
        "driver_for_tuktuk_details/",
        views.driver_for_tuktuk_details,
        name="driver_for_tuktuk_details",
    ),
    path("user_list/", views.user_list, name="user_list"),
    path("tuktuk_details/", views.tuktuk_details, name="tuktuk_details"),
    path("feed_reply/", views.feed_reply, name="feed_reply"),  # 13
    path("feed_reply_requests/", views.feed_reply_requests, name="feed_reply_requests"),
    path("user_feedback_reply/", views.user_feedback_reply, name="user_feedback_reply"),
    path(
        "user_feedback_reply_requests/",
        views.user_feedback_reply_requests,
        name="user_feedback_reply_requests",
    ),
    path(
        "feedback_details_post/",
        views.feedback_details_post,
        name="feedback_details_post",
    ),
    path("fare_estimation/", views.fare_estimation, name="fare_estimation"),
    path(
        "fare_estimation_requests/",
        views.fare_estimation_requests,
        name="fare_estimation_requests",
    ),
]
