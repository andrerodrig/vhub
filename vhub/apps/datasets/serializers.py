from rest_framework import serializers

from .models import Datasets
from vhub.apps.data.models import Data


class DatasetsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Datasets
        fields = ["id", "name", "created_at", "file", "owner"]
        read_only_fields = ["file", "created_at"]


class DatasetsDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    # data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return Data.objects.filter(dataset_id=obj.id).values()

    class Meta:
        model = Datasets
        fields = ["id", "name", "created_at", "file", "owner"]
        read_only_fields = ["file", "created_at"]
