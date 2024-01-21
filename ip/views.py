import requests

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import IP, Country
from .serializers import IPSerializer


class GetCountryAPIView(APIView):
    @transaction.atomic
    def get(self, request):
        ip_address = request.GET.get('ip')
        ip_address = ip_address.rstrip('/') if ip_address[-1] == '/' else ip_address
        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            return Response(
                data={'error': 'Invalid IP address format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ip, created = IP.objects.get_or_create(address=ip_address)

        if created:
            response = requests.get(f'https://api.country.is/{ip_address}')
            if response.status_code == 200:
                data = response.json()
                country_iso_code = data.get('country')
                country = Country.objects.filter(iso_code_2d=country_iso_code).first()

                if country is not None:
                    ip.country = country
                    ip.save()
                else:
                    ip.delete()
                    return Response(
                        data={'error': 'Country information not available for the provided IP'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                ip.delete()
                return Response(
                    data={'error': 'Bad request!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        ip_serializer = IPSerializer(ip)

        return Response(
            data={
                'ip': ip_serializer.data,
                'created': created,
            },
            status=status.HTTP_200_OK
        )
