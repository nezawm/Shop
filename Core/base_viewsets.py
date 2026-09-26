from django.db.models.deletion import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets


class BaseModelViewSet(viewsets.ModelViewSet):


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    def destroy(self, request, *args, **kwargs):

        try:

            instance = self.get_object()

            instance.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except ProtectedError:

            return Response(
                {
                    "success": False,
                    "message": "Delete operation failed.",
                    "error": "This object is referenced by other records."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": "Unexpected server error."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )