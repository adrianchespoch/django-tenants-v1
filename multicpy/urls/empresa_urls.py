from django.urls import path

from multicpy.views.empresa_views import (
    EmpresaView,
    EmpresaDetailView,
    EmpresaDetailViewByUuid,
)


urlpatterns = [
    path('', EmpresaView.as_view(), name='empresa'),
    path('<int:pk>/', EmpresaDetailView.as_view(), name='empresa-detail'),
    path('<str:uuid>/', EmpresaDetailViewByUuid.as_view(), name='empresa-detail-uuid'),
]
