from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, add_contact_view, view_contact_view 

# Create the router for API endpoints
router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoints for contacts
    path('', add_contact_view, name='add_contact'),
    path('view-contact/', view_contact_view, name='view_contact'),  
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
