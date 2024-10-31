from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm , CustomUserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from events_app.models import Event , BookingEvent
from django.db.models import Count , Q
from django.core.paginator import Paginator

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'account_app/profile.html')

@login_required
def profile_update_view(request):
    if request.method == "POST":
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'account_app/profile_update.html', {'user_form': user_form})


def home_view(request):
    search_query= request.GET.get('q')
    category_filter = request.GET.get('category', '') 
    events= Event.objects.annotate(booked_count= Count('booking_event')).select_related('creator')

    if search_query:
        events= events.filter(Q(name__icontains = search_query) | Q(date__icontains = search_query) | Q(location__icontains = search_query))

    if category_filter:
        events= events.filter(category=category_filter)

    user_event_ids= []
    if request.user.is_authenticated:
        user_bookings= BookingEvent.objects.filter(user=request.user)
        user_event_ids= [booking.event_id for booking in user_bookings]
    
    paginator = Paginator(events , 10)
    page_number = request.GET.get('page')
    paginated_events = paginator.get_page(page_number)

    return render(request, 'home.html',{'events':paginated_events,'user_event_ids':user_event_ids,'user':request.user, 'search_query':search_query,'category_filter':category_filter,'categories':Event.CATEGORY_CHOICES})
