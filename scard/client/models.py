from django.db import models
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files import File

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
