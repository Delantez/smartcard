from rest_framework import serializers
from .models import *

class ContactSerializer(serializers.ModelSerializer):
    qrcode = serializers.ImageField(use_url=True, required=False)  

    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'phone', 'email', 'organization',
            'job', 'address', 'country', 'qrcode'
        ]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['qrcode']  

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = '__all__'

class FlyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flyer
        fields = '__all__'