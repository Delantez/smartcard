from django.db import models
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.timezone import now

class Identity(models.Model):
    STAFF_CHOICES = [
        ('isstaff', 'Active'),
        ('notstaff', 'Inactive'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    validity_time = models.DateField()  # Changed to DateField
    status = models.BooleanField(default=True)  # Active (True) or Inactive (False)
    photo = models.ImageField(upload_to='media/photos/', blank=True, null=True)
    work = models.CharField(max_length=10, choices=STAFF_CHOICES, default='notstaff')  # Added field

    def save(self, *args, **kwargs):
        # Automatically update status based on `work` and `validity_time`
        if self.work == 'isstaff' and self.validity_time >= now().date():
            self.status = True  # valid staff with a valid date
        else:
            self.status = False  # Either not staff or the validity time has passed
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        # Dynamic property to check active status without relying on `status` field
        return self.work == 'isstaff' and self.validity_time >= now().date()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Flyer(models.Model):
    company = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='media/files/', blank=True, null=True)

    def __str__(self):
        return f"{self.company}"
    

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50)
    qrcode = models.ImageField(upload_to='media/qrcodes/', blank=True, null=True)


    def save(self, *args, **kwargs):
        # Building the vCard string with optional fields
        vcard = f"BEGIN:VCARD\nVERSION:4.0\n"
        vcard += f"N:{self.last_name};{self.first_name};;;\n"
        vcard += f"FN:{self.first_name} {self.last_name}\n"
        if self.phone:
            vcard += f"TEL;TYPE=CELL:{self.phone}\n"
        if self.email:
            vcard += f"EMAIL:{self.email}\n"
        if self.organization:
            vcard += f"ORG:{self.organization}\n"
        if self.job:
            vcard += f"TITLE:{self.job}\n"
        if self.address:
            vcard += f"ADR;TYPE=HOME:;;{self.address};;;;\n"
        vcard += "END:VCARD"

        # Generate the QR code
        qr = qrcode.make(vcard.strip())
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the qrcode field
        filename = f'{self.first_name}_{self.last_name}_qrcode.png'
        self.qrcode.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    product = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    qrcode = models.ImageField(upload_to='media/company_qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only generate QR code if it is a new company (no existing QR code or id)
        if not self.qrcode and not self.id:
            # Save the instance first to generate an ID (if it's new)
            super().save(*args, **kwargs)

            # Now that the object has an ID, generate the QR code
            current_site = Site.objects.get_current()
            domain = current_site.domain
            protocol = "https" if self.qrcode else "http"

            # Generate the absolute URL for this company
            company_url = f"{protocol}://{domain}{reverse('company_detail', args=[self.id])}"

            # Generate the QR code
            qr = qrcode.make(company_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            # Save the QR code image to the qrcode field
            filename = f'{self.company_name}_qrcode.png'
            self.qrcode.save(filename, File(buffer), save=False)

        # Now save the company with the generated QR code (if it's new)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.company_name    