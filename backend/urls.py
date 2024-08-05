from django.contrib import admin

# ### Swagger
import os
from rest_framework import permissions
from django.urls import path, re_path, include

from drf_yasg.views import get_schema_view

from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=os.environ.get('API_BASE_URL')
)


urlpatterns = [
    # ### Swagger ===============
    re_path(r'^api/v1/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    # ### Admin ===============
    path("admin/", admin.site.urls),


    # ### API
    path("api/v1/user/", include("users.urls.user_urls")),
    path("api/v1/extendedgroup/", include("users.urls.extended_group_urls")),
    path("api/v1/auth/", include("users.urls.auth_urls")),

    path("api/v1/empresa/", include("multicpy.urls.empresa_urls")),

    path("api/v1/suscripcion/", include("multicpy.urls.suscripcion_urls")),

    path("api/v1/book/", include("books.urls.book_urls")),

]
