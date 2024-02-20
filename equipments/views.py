from django.shortcuts import render
from .models import Equipment, Production, Qrcode
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect
from ipware import get_client_ip
import requests
from django.http import HttpResponseRedirect
# views.py
 


def index(request):
    
    equipments = Equipment.objects.all()
    production = Production.objects.all()
    qrcode_count = Qrcode.objects.all().count()
    return render(request,'equipments/index.html', {
        'production': production,
        'equipments': equipments,
        'qrcode_count': qrcode_count,
        'data': data, 
        'message': 'Data received and stored successfully'})

     

@csrf_exempt
def data(request):
    try:
        # Parse JSON data from the request
        
        data = json.loads(request.body.decode('utf-8'))
        

        # fetch equipment from database
        equipment = Equipment.objects.get(id=data['equipment'])
        print(equipment)
        # Store data in the database (Assuming you have a model named MyModel)
        Production.objects.create(
            equipment=equipment,
            input_desc=data['input_desc'],
            quantity=data['quantity'],
        )

        print('Activity saved for',equipment)
        # refresh the page
        equipments = Equipment.objects.all()
        return JsonResponse({'message': 'Data received and stored successfully'})

        # return JsonResponse({'message': 'Data received and stored successfully'})

    
    except json.JSONDecodeError as e:
        # Respond with an error message if JSON decoding fails

        return JsonResponse({'data': '', 'message': str(e)} )
        

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'data': '', 'message': str(e)} )

def qrcodeid(request):
    return render(request, 'equipments/qrcode.html')

def qrcode_detail(request):
    qrcodes = Qrcode.objects.all()
    return render(request, 'equipments/qrcode_detail.html', {
        'qrcodes': qrcodes
    })

@csrf_exempt
def get_client_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        print('Latitude:', latitude)
        print('Longitude:', longitude)
        Qrcode.objects.create(
            qrcode='id',
            latitude=latitude,
            longitude=longitude,
        )

        # Process the latitude and longitude as needed
        # For example, you can store them in the database, use them in your application, etc.

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def detail(request, equipment_id):
    # get equipment by id
    equipment = Equipment.objects.get(id=equipment_id)
    if request.method == 'POST':
        # validate date
        if request.POST.get('start_date') == '' or request.POST.get('end_date') == '':
            return render(request, 'equipments/detail.html', {
                'equipment': equipment,
                'error': 'Please select a start and end date'
            })
        # start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        start_date_str = request.POST.get('start_date')
        start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'), timezone=timezone.get_fixed_timezone(-480))
        # end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d') 
        end_date_str = request.POST.get('end_date')
        end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d'), timezone=timezone.get_fixed_timezone(-480))
        end_date_query = end_date + timedelta(days=1)
        print(start_date)
        print(end_date)
    else:
        start_date = datetime.now() - timedelta(days=2)
        end_date = datetime.now() 
        end_date_query = end_date + timedelta(days=1)
    production = Production.objects.filter(equipment=equipment_id, created_at__range=[start_date, end_date_query])
    
    # create two variables: one for created_at and one for quantity
    created_at = []
    quantity = []
    # loop through production and append created_at and quantity to the variables
    for prod in production:
        pacific_time = prod.created_at.astimezone(timezone.get_fixed_timezone(-480))
        created_at.append(pacific_time.strftime('%m-%d %H:%M'))
        quantity.append(prod.quantity)
    
    return render(request, 'equipments/detail.html', {
        'equipment': equipment,
        'production': production,
        'created_at': created_at,
        'quantity': quantity,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')

        })

# def tasks_detail(request, proj_id, task_id):
#     task = Task.objects.get(id=task_id)
#     profile = Profile.objects.get(user=request.user)
#     project = Project.objects.get(id=proj_id)
#     comment_form = CommentForm()
#     comments = Comment.objects.filter(task=task_id)
    
#     cannot_edit_task = not (profile.is_manager()
#                             or task.is_assignee(request.user))
#     user = request.user
#     return render(request, 'tasks/detail.html', {
#         'project': project,
#         'profile': profile,
#         'task': task,
#         'comments': comments,
#         'comment_form': comment_form,
#         'cannot_edit_task': cannot_edit_task,
#         'user': user

#     })