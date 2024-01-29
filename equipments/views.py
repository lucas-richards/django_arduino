from django.shortcuts import render
from .models import Equipment, Production
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.

@csrf_exempt
def index(request):
    try:
        # Parse JSON data from the request
        data = json.loads(request.body.decode('utf-8'))

        # Store data in the database (Assuming you have a model named MyModel)
        # Production.objects.create(data=json.dumps(data))
        print(data)
        render(request, 'equipments/index.html', {'data': data})

        # Respond with a JSON success message
        return JsonResponse({'message': 'Data received and stored successfully'})
    
    except json.JSONDecodeError as e:
        # Respond with an error message if JSON decoding fails
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def create_equipment(request):
    data = request.POST
    
    print(data)
    return JsonResponse({'message': 'Data received and stored successfully'})





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