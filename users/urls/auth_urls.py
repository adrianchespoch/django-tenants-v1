from django.urls import path

from users.views.auth_views import LoginCustomView, PermissionsCustomView, GroupPermissionsCustomView


urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),

    # permissions
    path("permissions/", PermissionsCustomView.as_view(), name="permissions"),
    path("permissions/<int:group_id>/",
         GroupPermissionsCustomView.as_view(), name="group_permissions"),
]
