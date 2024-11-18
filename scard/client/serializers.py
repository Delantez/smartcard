from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    qrcode = serializers.ImageField(use_url=True, required=False)  

    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'phone', 'email', 'organization',
            'job', 'address', 'country', 'qrcode'
        ]
