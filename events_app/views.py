from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .forms import EventForm
from .models import Event , BookingEvent
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

@login_required
def create_events_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event= form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'events_app/create_event.html', {'form': form})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.booking_event.count() >= event.capacity:
        return redirect('home')
    if BookingEvent.objects.filter(user=request.user, event=event).exists():
        return redirect('home')
    BookingEvent.objects.create(user=request.user, event=event)
    return redirect('home')

@login_required
def booked_events(request):
    user_bookings = BookingEvent.objects.filter(user=request.user).select_related('event')
    return render(request, 'events_app/booked_events.html', {'user_bookings': user_bookings})

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.creator and not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'events_app/update_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.creator and not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'events_app/delete_event.html', {'event': event})

# def event_list(request):
#     event_list = Event.objects.all()
#     paginator = Paginator(event_list, 10)
#     page_number = request.GET.get('page')
#     events = paginator.get_page(page_number)
#     return render(request, 'home.html', {'events': events})