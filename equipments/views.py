from django.shortcuts import render
from .models import Equipment, Production, Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect
import urllib.request
import json
import requests


 


def index(request):
    
    equipments = Equipment.objects.all()
    production = Production.objects.all()
    qrcode_count = Location.objects.all().count()
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

def qrcode_id(request):
    # with urllib.request.urlopen("https://geolocation-db.com/json") as url:
    #     data = json.loads(url.read().decode())
    #     data['qrcode'] = 'id'
    #     print(data)
    return render(request, 'equipments/qrcode.html')
    try:
        # Send a request to the ipinfo.io API to get information about the client's IP address
        response = requests.get('https://ipinfo.io')
        # Parse the JSON response
        data2 = response.json()
        # Extract relevant information (e.g., city, region, country)
        print('new data',data2)

    except Exception as e:
        print(f"Error: {e}")
    # Location(**data).save()
    Location.objects.create(
        qrcode='id2',
        city=data2['city'],
        state=data2['region'],
        country_name=data2['country'],
        postal=data2['postal'],
        IPv4 = data2['ip'],
        latitude=data2['loc'].split(',')[0],
        longitude=data2['loc'].split(',')[1],
    )
    return redirect('http://www.idlube.com')

def qrcode_tag(request):
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        data['qrcode'] = 'tag'
        print(data)
    Location(**data).save()
    return redirect('http://www.totalaccessgroup.com')

def qrcode_detail(request):
    locations = Location.objects.all()
    return render(request, 'equipments/qrcode_detail.html', {
        'locations': locations
    })

@csrf_exempt
def get_client_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        print('Latitude:', latitude)
        print('Longitude:', longitude)
        try:
            Location.objects.create(
                qrcode='id',
                latitude=latitude,
                longitude=longitude,
                IPv4='70.187.153.162',
                city='',
                state='',
                country_name='',
                postal='',
                

            )
        except Exception as e:
            print(f"Error: {e}")

        # Process the latitude and longitude as needed
        # For example, you can store them in the database, use them in your application, etc.

        return redirect('http://www.idlube.com')
    else:
        return redirect('http://www.idlube.com')

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