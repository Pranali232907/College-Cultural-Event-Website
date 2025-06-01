from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Event Categories"

class MediaCategory(models.Model):
    CATEGORY_CHOICES = [
        ('rangoli', 'Rangoli'),
        ('mehendi', 'Mehendi'),
        ('tshirt_painting', 'T-Shirt Painting'),
        ('face_painting', 'Face Painting'),
        ('nail_art', 'Nail Art'),
        ('dance', 'Dance'),
        ('singing', 'Singing'),
        ('fashion_show', 'Fashion Show'),
        ('instrument_playing', 'Instrument Playing'),
        ('cooking_without_fire', 'Cooking Without Fire'),
        ('treasure_hunt', 'Treasure Hunt'),
        ('glam_up', 'Glam Up'),
        ('prize_distribution', 'Prize Distribution'),
        ('group_alike_day', 'Group-Alike Day'),
        ('bollywood_day', 'Bollywood Day'),
        ('indo_western_day', 'Indo-Western Day'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name_plural = "Media Categories"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    rules = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Media(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_media/')
    category = models.ForeignKey(MediaCategory, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Media"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.event.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    submission_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_contacts')
    resolved_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
    
    def resolve(self, user, response):
        self.is_resolved = True
        self.response = response
        self.resolved_by = user
        self.resolved_date = timezone.now()
        self.save()
