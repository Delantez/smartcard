from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse

class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

def generate_qr_code(request, identity_id):
    # Generate the URL for the identity
    url = request.build_absolute_uri(f'/view_identity/{identity_id}/')

    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(buffer, content_type="image/png")


class FlyerViewSet(viewsets.ModelViewSet):
    queryset = Flyer.objects.all()
    serializer_class = FlyerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

def generate_flyer_qr(request, flyer_id):
    # Generate the QR code
    download_url = request.build_absolute_uri(f'/download_flyer/{flyer_id}/')
    qr = qrcode.make(download_url)
    
    # Create the HTTP response with appropriate headers
    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="flyer_qr_{flyer_id}.png"'
    qr.save(response, "PNG")
    return response


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
 
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Handle update but keep the QR code the same
        if 'qrcode' not in request.data:
            request.data['qrcode'] = instance.qrcode.name  # Ensure QR code isn't modified

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"message": "Company updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)

def add_contact_view(request): 
    return render(request, 'add_contact.html')  

def view_contact_view(request):
    contacts = Contact.objects.all()  # Fetch all contacts
    return render(request, 'view_contact.html', {'contacts': contacts})

def add_company_view(request):
    return render(request, 'add_company.html')  

def view_company_view(request):
    companies = Company.objects.all()  # Fetch all companys
    return render(request, 'view_company.html', {'companies': companies})

def edit_company_page(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'edit_company.html', {'company': company})

def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'company_detail.html', {'company': company})

def add_Id_view(request):
    return render(request, 'add_id.html')  

def view_Id_view(request):
    identities = Identity.objects.all()  # Fetch all Ids
    return render(request, 'view_id.html', {'identities': identities})

def view_identity(request, identity_id):
    identity = get_object_or_404(Identity, id=identity_id)
    return render(request, 'view_identity.html', {'identity': identity})

def edit_identity(request, pk):
    identity = get_object_or_404(Identity, pk=pk)
    return render(request, 'edit_identity.html', {'identity': identity})


def add_flyer_view(request):
    return render(request, 'add_flyer.html')  

def flyer_table_view(request):
    flyers = Flyer.objects.all()  # Fetch all Ids
    return render(request, 'flyer_table.html', {'flyers': flyers})

def view_flyer(request, flyer_id):
    flyer = get_object_or_404(Flyer, id=flyer_id) 
    return render(request, 'view_flyer.html', {'flyer': flyer})

def edit_flyer(request, pk):
    flyer = get_object_or_404(Flyer, pk=pk)
    return render(request, 'edit_flyer.html', {'flyer': flyer})

def download_flyer(request, flyer_id):
    flyer = get_object_or_404(Flyer, id=flyer_id)
    if flyer.file:
        return FileResponse(flyer.file.open('rb'), as_attachment=True, filename=flyer.file.name)
    else:
        return JsonResponse({'error': 'Flyer file not found'}, status=404)
