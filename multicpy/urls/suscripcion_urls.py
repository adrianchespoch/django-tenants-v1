from django.urls import path

from multicpy.views.suscripcion_views import (
    SuscripcionView,
    SuscripcionDetailView,
    SuscripcionDetailViewByUuid,
)


urlpatterns = [
    path('', SuscripcionView.as_view(), name='suscripcion'),
    path('<int:pk>/', SuscripcionDetailView.as_view(), name='suscripcion-detail'),
    path('<str:uuid>/', SuscripcionDetailViewByUuid.as_view(), name='suscripcion-detail-uuid'),
]
