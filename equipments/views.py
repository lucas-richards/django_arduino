from django.shortcuts import render
from .models import Equipment, Production
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.

@csrf_exempt
@require_POST
def index(request):
    data = request.POST.get('data')
    print('this is data',data)
    render(request, 'equipments/index.html')
    return JsonResponse({'message': 'Data received and stored successfully'})

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