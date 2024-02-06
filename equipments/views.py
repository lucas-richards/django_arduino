from django.shortcuts import render
from .models import Equipment, Production
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from django.utils import timezone
# views.py
import matplotlib
matplotlib.use('Agg') # Required to redirect the plot to a file
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
import os
from django.conf import settings
 


def index(request):
    
    equipments = Equipment.objects.all()
    production = Production.objects.all()
    return render(request,'equipments/index.html', {
        'production': production,
        'equipments': equipments,
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
    


def generate_graph(request):
    # Get the current date in your timezone
    current_date = timezone.now().date()

    # Get the data from the database for the current date
    data = Production.objects.filter(created_at__date=current_date)

    # Extract timestamps and corresponding values
    timestamps = []
    values = []

    # Loop through production and append created_at and quantity to the variables
    for prod in data:
        pacific_time = prod.created_at.astimezone(timezone.get_fixed_timezone(-480))
        timestamps.append(pacific_time)
        values.append(prod.quantity)

    # Convert time values to numerical format
    start_time = mdates.date2num(datetime.combine(current_date, datetime.min.time()))
    end_time = mdates.date2num(datetime.combine(current_date, datetime.max.time()))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set the x-axis format
    ax.xaxis.set_major_locator(MaxNLocator(nbins=20))  # adjust the number of x-axis ticks as needed
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    # Plot the production data
    ax.plot(timestamps, values, label='Production Data', color='green')

    # Create a horizontal line for the entire day
    ax.axhline(0, color='red', linestyle='--', xmin=start_time, xmax=end_time)

    # Customize the plot as needed
    ax.set_xlabel('Time')
    ax.set_ylabel('Production Quantity')
    ax.legend()

    # Save the plot to a temporary file or directly display it
    temp_file_path = './static/graph.png'
    plt.savefig(temp_file_path)
    print('Graph saved to', temp_file_path)
    plt.close()

    # Return the path to the saved image
    return render(request, 'graph.html', {'image_path': temp_file_path})


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