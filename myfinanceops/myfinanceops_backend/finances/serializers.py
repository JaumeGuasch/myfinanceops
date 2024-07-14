from rest_framework import serializers
from finances.models import User, StockOperation, FuturesOperation, FuturesOptionsOperation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'surnames', 'organization']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


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
