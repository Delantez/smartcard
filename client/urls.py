from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# Create the router for API endpoints
router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'identities', IdentityViewSet)
router.register(r'flyers', FlyerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoints for contacts
    path('', add_contact_view, name='add_contact'),
    path('view-contact/', view_contact_view, name='view_contact'), 
    path('add_company/', add_company_view, name='add_company'), 
    path('view-company/', view_company_view, name='view_company'), 
    path('company/edit/<int:pk>/', views.edit_company_page, name='company_edit'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('add_id/', add_Id_view, name='add_id'), 
    path('view-id/', view_Id_view, name='view_id'), 
    path('view_identity/<int:identity_id>/', views.view_identity, name='view_identity'),
    path('identity/edit/<int:pk>/', views.edit_identity, name='edit_identity'),
    path('generate_qr/<int:identity_id>/', views.generate_qr_code, name='generate_qr'),
    path('add_flyer/', add_flyer_view, name='add_flyer'), 
    path('flyer_table/', flyer_table_view, name='flyer_table'), 
    path('view_flyer/<int:flyer_id>/', views.view_flyer, name='view_flyer'),
    path('flyer/edit/<int:pk>/', views.edit_flyer, name='edit_flyer'),
    path('download_flyer/<int:flyer_id>/', views.download_flyer, name='download_flyer'),
    path('generate_flyer_qr/<int:flyer_id>/', views.generate_flyer_qr, name='generate_flyer_qr'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
