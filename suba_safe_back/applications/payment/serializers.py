# Imports de Third-Party Apps 
from rest_framework import serializers

# Imports de Modelos 
from applications.users.models import User
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    users = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            'id',
            #'user',
            'users',
            'description',
            'payment_type',
            'status_payment',
            'created',
            'modified',
        )
    
    def get_users(self, obj):
        query_set = User.payment_objects.users_per_payment(obj.id)
        serialized_users = UsersInPaymentSerializer(query_set, many=True).data
        return serialized_users


class UsersInPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'city',
        )


class PaymentProcessSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=130)
    payment_type = serializers.IntegerField()
    status_payment = serializers.IntegerField()
    auction = serializers.IntegerField()

    def validate_payment_type(self, value):

        if not(value==0 or value==1 or value==2):
            raise serializers.ValidationError('Ingrese un tipo de pago correcto')

        return value

    def validate_status_payment(self, value):
        
        if not(value == 0 or value == 1):
            raise serializers.ValidationError('Ingrese un estado de pago correcto')

        return value
        
