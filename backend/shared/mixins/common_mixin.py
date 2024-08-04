from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# authentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

# authorization
from django.core.exceptions import PermissionDenied

# cache
from django.core.cache import cache
import os
from backend.shared.utils.pagination_utils import get_pagination_parameters_rest
from backend.shared.utils.handle_rest_exception_helper import handle_rest_exception_helper
from backend.shared.utils.redis_utils import generate_cache_key, clear_cache_key_get_all


class AuthenticationViewMixin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AuthAdminViewMixin(APIView):
    authentication_classes = [TokenAuthentication]
    # is_staff - not is_superuser
    permission_classes = [IsAuthenticated, IsAdminUser]


class PermissionRequiredViewMixin(APIView):
    def check_permissions(self, request):
        app_table_name = self.service.model._meta.db_table
        table_name = app_table_name.split('_')[1]
        app_name = app_table_name.split('_')[0]
        if request.method == 'GET':
            if not request.user.has_perm(f'{app_name}.view_{table_name}'):
                raise PermissionDenied()
        elif request.method == 'POST':
            if not request.user.has_perm(f'{app_name}.add_{table_name}'):
                raise PermissionDenied()
        elif request.method in ['PUT', 'PATCH']:
            if not request.user.has_perm(f'{app_name}.change_{table_name}'):
                raise PermissionDenied()
        elif request.method == 'DELETE':
            if not request.user.has_perm(f'{app_name}.delete_{table_name}'):
                raise PermissionDenied()
        return super().check_permissions(request)


class CacheViewMixin:
    def get_cache_key(self, filter_params):
        return generate_cache_key(filter_params=filter_params, model_name=self.service.model.__name__)

    def get_cached_data(self, cache_key):
        return cache.get(cache_key)

    def set_cached_data(self, cache_key, data):
        cache.set(cache_key, data, timeout=int(
            os.environ.get('REDIS_TIMEOUT')))

    def clear_cache(self):
        model_name = self.service.model.__name__
        cache.delete(f"{model_name}_all")
        cache.delete(f"{model_name}_one")
        clear_cache_key_get_all(model_name)


class ListViewMixin(CacheViewMixin):
    def get(self, request):
        try:
            filter_params, page_number, page_size = get_pagination_parameters_rest(
                request)
            cache_key = self.get_cache_key(filter_params)
            cache_data = self.get_cached_data(cache_key)

            if cache_data:
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Elementos paginados correctamente',
                        'data': {
                            'meta': cache_data['meta'],
                            'items': cache_data['data'],
                        }
                    },
                    status=status.HTTP_200_OK
                )

            serialized_instances = self.service.find_all(
                filter_params, page_number, page_size)
            self.set_cached_data(
                cache_key, {
                    'meta': serialized_instances['meta'], 'data': serialized_instances['data']}
            )

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elementos paginados correctamente',
                    'data': {
                        'meta': serialized_instances['meta'],
                        'items': serialized_instances['data'],
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return handle_rest_exception_helper(e)


class CreateViewMixin(CacheViewMixin):
    def post(self, request):
        try:
            serialized_instance = self.service.create(request.data)
            self.clear_cache()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Elemento creado correctamente',
                    'data': serialized_instance
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return handle_rest_exception_helper(e)


# UUID
class RetrieveViewMixin(CacheViewMixin):
    def get(self, request, uuid):
        cache_key = f"{self.service.model.__name__}_one"
        cache_data = self.get_cached_data(cache_key)

        if cache_data:
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elemento encontrado',
                    'data': cache_data
                },
                status=status.HTTP_200_OK
            )

        try:
            serialized_instance = self.service.find_one_by_uuid(uuid)
            self.set_cached_data(cache_key, serialized_instance)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elemento encontrado',
                    'data': serialized_instance
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return handle_rest_exception_helper(e)


class RetrievePkViewMixin(CacheViewMixin):
    def get(self, request, pk):
        cache_key = f"{self.service.model.__name__}_one"
        cache_data = self.get_cached_data(cache_key)

        if cache_data:
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elemento encontrado',
                    'data': cache_data
                },
                status=status.HTTP_200_OK
            )

        try:
            serialized_instance = self.service.find_one(pk)
            self.set_cached_data(cache_key, serialized_instance)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elemento encontrado',
                    'data': serialized_instance
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return handle_rest_exception_helper(e)


class UpdateViewMixin(CacheViewMixin):
    def patch(self, request, pk):
        try:
            serialized_instance = self.service.update(pk, request.data)
            self.clear_cache()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Elemento actualizado correctamente',
                    'data': serialized_instance
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return handle_rest_exception_helper(e)


class DestroyViewMixin(CacheViewMixin):
    def delete(self, request, pk):
        try:
            self.service.delete(pk)
            self.clear_cache()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return handle_rest_exception_helper(e)


# ### Sales Mixins ===================================
