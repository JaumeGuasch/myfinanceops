from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation
from rest_framework import serializers

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'email', 'name', 'surnames', 'organization', 'is_active', 'is_staff']


class StockOperationSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(source='market.name', read_only=True)

    class Meta:
        model = StockOperation
        fields = '__all__'


class FuturesOperationSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(source='market.name', read_only=True)

    class Meta:
        model = FuturesOperation
        fields = '__all__'


class FuturesOptionsOperationSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(source='market.name', read_only=True)

    class Meta:
        model = FuturesOptionsOperation
        fields = '__all__'


class UnifiedOperationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, StockOperation):
            serializer = StockOperationSerializer(instance)
        elif isinstance(instance, FuturesOperation):
            serializer = FuturesOperationSerializer(instance)
        elif isinstance(instance, FuturesOptionsOperation):
            serializer = FuturesOptionsOperationSerializer(instance)
        else:
            raise Exception("Unknown operation type")
        return serializer.data
