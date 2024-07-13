from django.shortcuts import render
from .models import CropDetails, AssignmentDetails, WorkerDetails, EquipmentDetails, SupplierDetails
from datetime import date
from django.db.models import Count

def dashboard(request):
    # Get counts for At A Glance section
    crop_count = CropDetails.objects.count()
    task_count = AssignmentDetails.objects.count()
    worker_count = WorkerDetails.objects.count()

    # Get current production information
    current_crops = CropDetails.objects.filter(planting_date__lte=date.today(), harvesting_date__gte=date.today())
    
    # Get urgent and upcoming tasks
    urgent_tasks = AssignmentDetails.objects.filter(end_date__lte=date.today()).order_by('end_date')[:3]
    upcoming_tasks = AssignmentDetails.objects.filter(end_date__gt=date.today()).order_by('end_date')[:3]

    context = {
        'crop_count': crop_count,
        'task_count': task_count,
        'worker_count': worker_count,
        'current_crops': current_crops,
        'urgent_tasks': urgent_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'dashboard.html', context)

def crop(request):
    crops = CropDetails.objects.all()
    return render(request, 'crop.html',  {'crops': crops})

def task(request):
    assignments = AssignmentDetails.objects.all()
    return render(request, 'task.html', {'assignments': assignments})

def inventory(request):
    return render(request, 'inventory.html')

def worker(request): 
    workers = WorkerDetails.objects.all()
    return render(request, 'worker.html',  {'workers': workers})

def equipment(request):
    equipments = EquipmentDetails.objects.all()
    return render(request, 'equipment.html', {'equipments': equipments})

def supplier(request):
    suppliers = SupplierDetails.objects.all()
    return render(request, 'supplier.html', {'suppliers': suppliers})


