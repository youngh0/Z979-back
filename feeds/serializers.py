from rest_framework import serializers

from feeds.models import Feed, FeedImage


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

class FeedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =FeedImage
        fields = '__all__'