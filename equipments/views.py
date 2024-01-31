from django.shortcuts import render
from .models import Equipment, Production
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import html
from django.views.decorators.http import require_POST
from datetime import datetime, timezone
from datetime import datetime, timedelta

# Create your views here.


@csrf_exempt
def index(request):
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
        return render(request,'equipments/index.html', {
            'equipments': equipments,
            'data': data, 
            'message': 'Data received and stored successfully'})

        # return JsonResponse({'message': 'Data received and stored successfully'})

    
    except json.JSONDecodeError as e:
        # Respond with an error message if JSON decoding fails

        equipments = Equipment.objects.all()
        return render(request,'equipments/index.html', {
            'equipments': equipments,
            'data': '', 
            'message': 'Invalid JSON data'})
        

    except Exception as e:
        # Handle other exceptions
        equipments = Equipment.objects.all()
        return render(request,'equipments/index.html', {'data': '', 'message': str(e)} )
        

@csrf_exempt
def create_equipment(request):
    data = request.POST
    
    print(data)
    return JsonResponse({'message': 'Data received and stored successfully'})


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
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').replace(tzinfo=timezone.utc)
        print(start_date)
        print(end_date)
    else:
        start_date = datetime.now(timezone.utc) - timedelta(days=2)
        end_date = datetime.now().replace(tzinfo=timezone.utc)
    production = Production.objects.filter(equipment=equipment_id, created_at__range=[start_date, end_date])
    
    # create two variables: one for created_at and one for quantity
    created_at = []
    quantity = []
    # loop through production and append created_at and quantity to the variables
    for prod in production:
        created_at.append(prod.created_at.strftime('%m-%d %H:%M'))
        quantity.append(prod.quantity)
    return render(request, 'equipments/detail.html', {
        'equipment': equipment,
        'production': production,
        'created_at': created_at,
        'quantity': quantity,

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