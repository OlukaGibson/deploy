from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api_url/<str:pk>/', views.api_url),
    path('display_firmware_update/', views.display_firmware_update, name='display_firmware_update'),
    path('update_selected_values/', views.update_selected_values, name='update_selected_values'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)