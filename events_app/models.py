from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    CATEGORY_CHOICES = [
    ('conference', 'Conference'),
    ('concert', 'Concert'),
    ('workshop', 'Workshop'),
    ('seminar', 'Seminar'),
    ('exhibition', 'Exhibition'),
    ('webinar', 'Webinar'),
    ('networking', 'Networking Event'),
    ('festival', 'Festival'),
    ('theater', 'Theater Performance'),
    ('film', 'Film Screening'),
    ('meetup', 'Meetup'),
    ('fundraiser', 'Fundraiser'),
    ('sport', 'Sporting Event'),
    ('class', 'Class'),
    ('retreat', 'Retreat'),
    ('hackathon', 'Hackathon'),
    ('fair', 'Fair'),
    ('open_house', 'Open House'),
    ('panel', 'Panel Discussion'),
    ('competition', 'Competition'),
    ('trade_show', 'Trade Show'),
    ('book_reading', 'Book Reading'),
    ('community_service', 'Community Service Event'),
    ('culinary', 'Culinary Event'),
    ('art_show', 'Art Show'),
    ('science_fair', 'Science Fair'),
    ('fashion_show', 'Fashion Show'),
    ('virtual_event', 'Virtual Event'),
    ('cultural_event', 'Cultural Event'),
    ('pet_expo', 'Pet Expo'),
    ]

    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name

class BookingEvent(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking_event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_user')

    class Meta:
        unique_together = ('user', 'event')