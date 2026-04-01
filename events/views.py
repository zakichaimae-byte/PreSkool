from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.contrib import messages

def event_list(request):
    events = Event.objects.all().order_by('date', 'start_time')
    return render(request, 'events/list.html', {'events': events})

def event_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        responsible = request.POST.get('responsible')
        event_type = request.POST.get('event_type')
        
        Event.objects.create(
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            responsible=responsible,
            event_type=event_type
        )
        messages.success(request, "Évènement ajouté.")
        return redirect('event_list')
    return render(request, 'events/add.html')
