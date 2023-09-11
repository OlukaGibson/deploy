from rest_framework import serializers
from .models import FirmwareUpdate

class FirmwareUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareUpdate
        fields = '__all__'
