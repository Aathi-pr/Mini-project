"""
URL configuration for TukTukGO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Guest import views

urlpatterns = [
    path("Admin/", admin.site.urls),
    path("", views.home_page),  # 1
    path("sign_up_page/", views.sign_up_page),  # 2
    path("validate_login/", views.validate_login),  # 3
    path("admin_process/", views.admin_process),
    path("change_pass/", views.change_pass),  # 4
    path("change_pass1/", views.change_pass_1),  # 5
    path("tuktuk_registration/", views.tuktuk_registration),  # 6
    path("tuktuk_registration1/", views.tuktuk_registration_1),  # 7
    path("driver_process/", views.driver_process),
    path("tuktuk_driver_registration/", views.tuktuk_driver_registration),  # 8
    path("tuktuk_driver_registration1/", views.tuktuk_driver_registration_1),  # 9
    path("tuktuk_allot/", views.tuktuk_allot),  # 10
    path("tuktuk_allot_1/", views.tuktuk_allot_1),  # 11
    path("tuktuk_allot_2/", views.tuktuk_allot_2),  # 12
    path("tuktuk_allot_3/", views.tuktuk_allot_3),  # 13
    path("user_process/", views.user_process),
    path("tuktuk_user_login/", views.tuktuk_user_login),  # 14
    path("tuktuk_user_login_requests/", views.tuktuk_user_login_requests),  # 15
    path("user_change_pass/", views.user_change_pass),  # 16
    path("user_change_pass_1/", views.user_change_pass_1),  # 17
    path("driver_change_pass/", views.driver_change_pass),  # 18
    path("driver_change_pass_1/", views.driver_change_pass_1),  # 19
    path("tuktuk_details/", views.tuktuk_details),  # 20
    path("feedback/", views.feedback),  # 21
    path("feedback_1/", views.feedback_1),  # 22
    path("feed_reply/", views.feed_reply),  # 23
    path("feed_reply_requests/", views.feed_reply_requests),  # 24
    path("feedback_details_post/", views.feedback_details_post),  # 25
    path("user_feedback/", views.user_feedback),  # 26
    path("user_feedback_1/", views.user_feedback_1),  # 27
    path("user_feedback_reply/", views.user_feedback_reply),  # 28
    path("user_feedback_reply_requests/", views.user_feedback_reply_requests),  # 29
    path("user_feedback_details_post/", views.user_feedback_details_post),  # 30
    path("booking_page/", views.booking_page, name="booking_page"),  # 31
    path(
        "calculate_distance_and_allot_auto/",
        views.calculate_distance_and_allot_auto,
        name="calculate_distance_and_allot_auto",
    ),  # 32
    path(
        "request_tuktuk_and_tuktuk_driver/", views.request_tuktuk_and_tuktuk_driver
    ),  # 33
    path("response_for_tuktuk/", views.response_for_tuktuk),  # 34
    path("response_for_tuktuk_requests/", views.response_for_tuktuk_requests),  # 35
    path("fare_estimation/", views.fare_estimation),  # 36
    path("fare_estimation_requests/", views.fare_estimation_requests),  # 37
    path("ride_details/", views.ride_details, name="ride_details"),  # 38
    path("on_going_ride/", views.on_going_ride),  # 39
    path("on_going_ride_requests/", views.on_going_ride_requests),  # 40
    path("user_list/", views.user_list),  # 41
    path("tuktuk_for_driver/", views.tuktuk_for_driver),  # 42
    path("tuktuk_for_driver_details/", views.tuktuk_for_driver_details),  # 43
    path("driver_for_tuktuk/", views.driver_for_tuktuk),  # 44
    path("driver_for_tuktuk_details/", views.driver_for_tuktuk_details),  # 45
    path(
        "check_driver_response/",
        views.check_driver_response,
        name="check_driver_response",
    ),
    path("map_view/", views.map_view),
    path("driver_ride_details/", views.driver_ride_details),
    path("star_feedback/", views.star_feedback),  # 46
    path("receipt/", views.receipt),
    path("receipt_requests/", views.receipt_requests),
    path("receipt_requests_confirm/", views.receipt_requests_confirm),
    path("payment_history/", views.payment_history),
    path("feedback_view/", views.feedback_view),
    path("feedback_view_requests/", views.feedback_view_requests),
    path("driver_feedback_view/", views.driver_feedback_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
