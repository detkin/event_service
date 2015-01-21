from rest_framework import serializers
from event_service.models import Event


class EventSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    hostname = serializers.CharField(max_length=255)
    string = serializers.CharField(max_length=255)
    created_on = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Event` instance, given the validated data.
        """
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.string = validated_data.get('string', instance.string)
        instance.created_on = validated_data.get('created_on',
                                                 instance.created_on)
        instance.save()
        return instance