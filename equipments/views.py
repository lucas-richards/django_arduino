from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "equipments/index.html")

# create
def create(request):
    return render(request, "equipments/create.html")

    