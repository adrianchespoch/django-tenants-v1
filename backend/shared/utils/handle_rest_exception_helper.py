from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.exceptions import NotAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.core.exceptions import FieldError


import traceback


from backend.shared.serializers.serializers import (
    ErrorResponseDTO,
    NotFoundErrorResponseDTO,
    UnauthorizedErrorResponseDTO,
)
from backend.shared.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from backend.shared.exceptions.invalid_fields_exception import InvalidFieldsException
from backend.shared.exceptions.unauthorized_exception import UnauthorizedException
from backend.shared.exceptions.bad_request_exception import BadRequestException
from backend.shared.exceptions.conflicts_exception import ConflictsException
from backend.shared.exceptions.locked_request_exception import LockedRequestException

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


def handle_rest_exception_helper(exc):

    if isinstance(exc, NotAuthenticated) or isinstance(exc, UnauthorizedException):
        error = UnauthorizedErrorResponseDTO(
            status=status.HTTP_401_UNAUTHORIZED, message=str(exc), data=exc.data if hasattr(exc, 'data') else None
        )
        return Response(error.__dict__, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, Token.DoesNotExist) or isinstance(exc, AuthenticationFailed):
        error = UnauthorizedErrorResponseDTO(
            status=status.HTTP_401_UNAUTHORIZED, message=str(exc)
        )
        return Response(error.__dict__, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, PermissionDenied):
        error = UnauthorizedErrorResponseDTO(
            status=status.HTTP_403_FORBIDDEN, message='Permission denied'
        )
        return Response(error.__dict__, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, ResourceNotFoundException):
        not_found = NotFoundErrorResponseDTO(
            status=status.HTTP_404_NOT_FOUND,
            message=str(exc),
        )
        # JsonResponse 'cause own 404 middleware
        return JsonResponse(not_found.__dict__, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, LockedRequestException):
        locked_request = ErrorResponseDTO(
            status=status.HTTP_423_LOCKED,
            message=str(exc),
        )
        return Response(locked_request.__dict__, status=status.HTTP_423_LOCKED)
    elif isinstance(exc, InvalidFieldsException):
        invalid_fields = [
            f"{field}: {error}" for field, errors in exc.fields for error in errors
        ]
        bad_request = ErrorResponseDTO(
            status=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            invalid_fields=invalid_fields,
        )
        return Response(bad_request.__dict__, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, BadRequestException):
        bad_request = ErrorResponseDTO(
            status=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            data=exc.data,
        )
        return Response(bad_request.__dict__, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, FieldError):  # handle order_by field error
        bad_request = ErrorResponseDTO(
            status=status.HTTP_400_BAD_REQUEST,
            message='Invalid filter field',
        )
        return Response(bad_request.__dict__, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, ConflictsException):
        conflict = ErrorResponseDTO(
            status=status.HTTP_409_CONFLICT,
            message=str(exc),
            data=exc.data,
        )
        return Response(conflict.__dict__, status=status.HTTP_409_CONFLICT)
    # does not override the DRF serializer errors response
    elif isinstance(exc, ValidationError):
        validation_error = ErrorResponseDTO(
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid fields",
            invalid_fields=exc.messages
        )
        return Response(validation_error.__dict__, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('--------- UNEXPECTED ERROR ---------')
        print(traceback.format_exc())
        message = ''
        try:
            message = str(exc.message if hasattr(exc, 'message') else exc)
        except:
            message = 'Unexpected error'

        error = ErrorResponseDTO(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
        )
        return Response(error.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
