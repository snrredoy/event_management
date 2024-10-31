from django.urls import path
from . import views

urlpatterns = [
    path('create_events/',views.create_events_view,name = "create_events"),
    path('book_event/<int:event_id>/', views.book_event,name="book_event"),
    path('booked_events/', views.booked_events,name="booked_events"),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]