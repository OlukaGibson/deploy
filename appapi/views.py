from django.http import JsonResponse
from .models import FirmwareUpdate
from .serializers import FirmwareUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


# @api_view(['GET',])
# def api_url(request,device_id):
#     if request.method == 'GET':
#         firmware_updates = FirmwareUpdate.objects.filter(device_id=device_id).order_by('-uploaded_at').first()
#         serializer = FirmwareUpdateSerializer(firmware_updates, many=True)
#         return JsonResponse(serializer.data, safe=False) 
    
# device_api/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import DeviceData

def get_device_data(request, device_id):
    device_data = get_object_or_404(DeviceData, device_id=device_id)
    
    # Serialize the data into JSON
    data = {
        'version': device_data.version,
        'description': device_data.description,
        'spvValue': device_data.spvValue,
        'batteryValue': device_data.batteryValue,
        'firmware': device_data.firmware,
        'device_id': device_data.device_id,
        'uploaded_at': device_data.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    return JsonResponse(data)



@login_required
def display_firmware_update(request):
    firmware_updates = FirmwareUpdate.objects.all().order_by('-device_id')

    # Check if a grouping parameter is provided in the URL
    group_by = request.GET.get('group_by')

    if group_by == 'firmware':
        firmware_updates = firmware_updates.order_by('firmware')
    elif group_by == 'batteryValue':
        firmware_updates = firmware_updates.order_by('batteryValue')
    elif group_by == 'spvValue':
        firmware_updates = firmware_updates.order_by('spvValue')

    context = {
        'firmware_updates': firmware_updates,
        'group_by': group_by
        }
    
    return render(request, 'appapi/firmware_update.html', context)

@login_required
def update_selected_values(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_updates')
        field_to_edit = request.POST.get('field_to_edit')
        new_value = request.POST.get(field_to_edit)

        if selected_ids and field_to_edit in ('spvValue', 'batteryValue'):
            field_to_update = {field_to_edit: new_value}
            FirmwareUpdate.objects.filter(id__in=selected_ids).update(**field_to_update)

            # Respond with a success message (you can customize this JSON response)
            response_data = {'message': f'{field_to_edit} updated successfully.'}
            return JsonResponse(response_data)

    # If the form submission is invalid or no updates were made, respond with an error message
    response_data = {'error': 'Invalid form submission or no updates were made.'}
    return JsonResponse(response_data, status=400)

# views.py
from django.shortcuts import render, redirect
from .forms import FirmwareUpdateForm  # Import the form

def add_firmware_update(request):
    if request.method == 'POST':
        form = FirmwareUpdateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('firmware-update-list')
    else:
        form = FirmwareUpdateForm()

    return render(request, 'appapi/add_firmware_update.html', {'form': form})
