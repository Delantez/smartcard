from rest_framework import viewsets
from .models import Contact
from .serializers import ContactSerializer
from django.shortcuts import render

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
def add_contact_view(request):
    return render(request, 'add_contact.html')  

def view_contact_view(request):
    contacts = Contact.objects.all()  # Fetch all contacts
    return render(request, 'view_contact.html', {'contacts': contacts})