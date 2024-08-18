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
    path("", views.homePage),  # 1
    path("signUpPage/", views.signUpPage),  # 2
    path("validateLogin/", views.validateLogin),  # 3
    path("adminProcess/", views.adminProcess),
    path("changePass/", views.changePass),  # 4
    path("changePass1/", views.changePass1),  # 5
    path("tuktukRegistration/", views.tuktukRegistration),  # 6
    path("tuktukRegistration1/", views.tuktukRegistration1),  # 7
    path("driverProcess/", views.driverProcess),
    path("tuktukDriverRegistration/", views.tuktukDriverRegistration),  # 8
    path("tuktukDriverRegistration1/", views.tuktukDriverRegistration1),  # 9
    path("tuktukAllot/", views.tuktukAllot),  # 10
    path("tuktukAllot1/", views.tuktukAllot1),  # 11
    path("tuktukAllot2/", views.tuktukAllot2),  # 12
    path("tuktukAllot3/", views.tuktukAllot3),  # 13
    path("userProcess/", views.userProcess),
    path("tuktukUserLogin/", views.tuktukUserLogin),  # 14
    path("tuktukUserLoginRequests/", views.tuktukUserLoginRequests),  # 15
    path("userChangePass/", views.userChangePass),  # 16
    path("userChangePass1/", views.userChangePass1),  # 17
    path("driverChangePass/", views.driverChangePass),  # 18
    path("driverChangePass1/", views.driverChangePass1),  # 19
    path("tuktukDetails/", views.tuktukDetails),  # 20
    path("feedback/", views.feedback),  # 21
    path("feedback1/", views.feedback1),  # 22
    path("feedReply/", views.feedReply),  # 23
    path("feedReplyRequests/", views.feedReplyRequests),  # 24
    path("feedbackDetailsPost/", views.feedbackDetailsPost),  # 25
    path("userFeedback/", views.userFeedback),  # 26
    path("userFeedback1/", views.userFeedback1),  # 27
    path("userFeedbackReply/", views.userFeedbackReply),  # 28
    path("userFeedbackReplyRequests/", views.userFeedbackReplyRequests),  # 29
    path("userFeedbackDetailsPost/", views.userFeedbackDetailsPost),  # 30
    path("bookingPage/", views.bookingPage, name="bookingPage"),  # 31
    path(
        "calculate_distance_and_allot_auto/",
        views.calculate_distance_and_allot_auto,
        name="calculate_distance_and_allot_auto",
    ),  # 32
    path("requetTuktukAndTuktukDriver/", views.requetTuktukAndTuktukDriver),  # 33
    path("responseForTuktuk/", views.responseForTuktuk),  # 34
    path("responseForTuktukRequests/", views.responseForTuktukRequests),  # 35
    path("fareEstimation/", views.fareEstimation),  # 36
    path("fareEstimationRequets/", views.fareEstimationRequets),  # 37
    path("rideDetails/", views.rideDetails, name="rideDetails"),  # 38
    path("onGoingRide/", views.onGoingRide),  # 39
    path("onGoingRideRequests/", views.onGoingRideRequests),  # 40
    path("userList/", views.userList),  # 41
    path("tuktukForDriver/", views.tuktukForDriver),  # 42
    path("tuktukForDriverDetails/", views.tuktukForDriverDetails),  # 43
    path("driverForTuktuk/", views.driverForTuktuk),  # 44
    path("driverForTuktukDetails/", views.driverForTuktukDetails),  # 45
    path("checkDriverResponse/", views.checkDriverResponse, name="checkDriverResponse"),
    path("mapView/", views.mapView),
    path("driverRideDetails/", views.driverRideDetails),
    path("starFeedback/", views.starFeedback),  # 46
    path("receipt/", views.receipt),
    path("receiptRequests/", views.receiptRequests),
    path("receiptRequestsConfirm/", views.receiptRequestsConfirm),
    path("paymentHistory/", views.paymentHistory),
    path("feedbackView/", views.feedbackView),
    path("feedbackViewRequests/", views.feedbackViewRequests),
    path("driverFeedbackView/", views.driverFeedbackView),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
