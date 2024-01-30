from django.shortcuts import render
from .models import Equipment, Production
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


@csrf_exempt
def index(request):
    try:
        # Parse JSON data from the request
        
        data = json.loads(request.body.decode('utf-8'))

        # fetch equipment from database
        print('data[equipment]',data['equipment'])
        print('data[input_desc]',data['input_desc'])
        # Store data in the database (Assuming you have a model named MyModel)
        is_created = Production.objects.create(
            equipment=data['equipment'],
            input_desc=data['input_desc'],
            frequency=data['frequency'],
            quantity=data['quantity'],
        )

        print('is_created',is_created)

        # print(data)
        return JsonResponse({'message': 'Data received and stored successfully'})

    
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
    equipment = Equipment.objects.filter(id=equipment_id)
    production = Production.objects.filter(equipment=equipment_id)
    return render(request, 'equipments/detail.html', {
        'equipment': equipment,
        'production': production

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