from rest_framework import serializers
from .models import SpyCat, Mission, Target
from .utils import validate_breed

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = "__all__"

    def validate_breed(self, value):
        validate_breed(value)
        return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "complete"]


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(
        queryset=SpyCat.objects.all(),
        required=False
    )

    class Meta:
        model = Mission
        fields = ["id", "cat", "complete", "targets"]

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for target_data in targets_data:
            target_id = target_data.get('id')
            if target_id:
                target = Target.objects.get(id=target_id, mission=instance)
                for attr, value in target_data.items():
                    setattr(target, attr, value)
                target.save()
            else:
                Target.objects.create(mission=instance, **target_data)

        return instance
