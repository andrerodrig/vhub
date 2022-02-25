from rest_framework import serializers

from .models import Data


class DataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Data
        fields = [
            "id",
            "hostname",
            "ip_address",
            "title",
            "severity",
            "cvss",
            "publication_date",
            "solved",
            "owner"
        ]


class DataDetailSerializer(serializers.ModelSerializer):
    dataset = serializers.ReadOnlyField(source="dataset.id")

    class Meta:
        model = Data
        fields = [
            "id",
            "hostname",
            "ip_address",
            "title",
            "severity",
            "cvss",
            "publication_date",
            "solved",
            "dataset"
        ]
        read_only_fields = [
            "id",
            "hostname",
            "ip_address",
            "title",
            "severity",
            "cvss",
            "publication_date"
        ]
