from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests


ESP32_IP = "192.168.232.163:8000"
# def index(request):
#     return render(request, 'control/control.html')
#
# def control_led(request, state):
#     if state not in ['on', 'off']:
#         return HttpResponse('Invalid state', status=400)
#     try:
#         response = requests.get(f'http://{ESP32_IP}/led/{state}')
#         if response.status_code == 200:
#             return HttpResponse(f'LED turned {state}', status=200)
#         else:
#             return HttpResponse('Failed to control LED', status=500)
#     except requests.exceptions.RequestException as e:
#         return HttpResponse(str(e), status=500)


# def control_esp32(request):
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         esp32_ip = "http://192.168.232.162"  # آدرس IP برد ESP32-CAM
#
#         if action == 'on':
#             response = requests.get(f"{esp32_ip}/led_on")
#         elif action == 'off':
#             response = requests.get(f"{esp32_ip}/led_off")
#         else:
#             response = None
#
#         if response:
#             return JsonResponse({"response": response.text})
#         else:
#             return JsonResponse({"response": "Invalid action"})
#
#     return render(request, 'control.html')

ESP32_SERVER_URL = "http://192.168.232.163:8000/"

def control_esp32(request):
    context = {
        'status': get_arduino_status()
    }
    return render(request, 'control/control.html', context)

def toggle_led(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        send_command_to_arduino(command)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def get_arduino_status():
    try:
        response = requests.get(ESP32_SERVER_URL)
        if response.status_code == 200:
            return response.json().get('status')
    except requests.RequestException as e:
        print(f"Error fetching Arduino status: {str(e)}")
    return 'Unknown'

def send_command_to_arduino(command):
    try:
        response = requests.post(ESP32_SERVER_URL, json={'command': command})
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(f"Error sending command to Arduino: {str(e)}")
    return False
