from rest_framework import serializers

from .models import Country, IP


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'iso_code_2d',
            'iso_code_3d',
        )


class IPSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = IP
        fields = (
            'id',
            'address',
            'country',
        )
