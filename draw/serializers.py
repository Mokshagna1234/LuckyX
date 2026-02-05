from rest_framework import serializers
from .models import LuckyDraw, Participant


class LuckyDrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuckyDraw
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
