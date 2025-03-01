from rest_framework import serializers
from .models import Fashion, Contact, Fashion2


class FashionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fashion
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class Fashion2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fashion2
        fields = '__all__'



