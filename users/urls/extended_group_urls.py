from django.urls import path

from users.views.extended_group_views import (
    ExtendedGroupView,
    ExtendedGroupDetailView,
    ExtendedGroupDetailViewByUuid,
)


urlpatterns = [
    path('', ExtendedGroupView.as_view(), name='extended_group'),
    path('<int:pk>/', ExtendedGroupDetailView.as_view(),
         name='extended_group-detail'),
    path('<str:uuid>/', ExtendedGroupDetailViewByUuid.as_view(),
         name='extended_group-detail-uuid'),
]
