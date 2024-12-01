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

# from django.contrib import admin
from django.urls import include, path

from Guest import views

urlpatterns = [
    # path("Admin/", admin.site.urls),
    path("", views.home_page),  # 1
    path("sign_up_page/", views.sign_up_page, name="sign_up_page"),  # 2
    path("validate_login/", views.validate_login, name="validate_login"),
    path("Admin/", include("Admin.urls")),  # 3
    path("Driver/", include("Driver.urls")),
    path("User/", include("User.urls")),
    path("tuktuk_user_login/", views.tuktuk_user_login, name="tuktuk_user_login"),  # 14
    path(
        "tuktuk_user_login_requests/",
        views.tuktuk_user_login_requests,
        name="tuktuk_user_login_requests",
    ),  # 15
    path("fare_data/", views.fare_data, name="fare_data"),

    path("privacy_conditions/", views.privacy_conditions,name="privacy_conditions"),
]
