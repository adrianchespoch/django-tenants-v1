from django.urls import path

from users.views.user_views import (
    UserView
)


urlpatterns = [
    path('', UserView.as_view(), name='user'),
]
