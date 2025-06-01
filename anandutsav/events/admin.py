from django.contrib import admin
from .models import Event, EventCategory, Media, MediaCategory, Review, Contact, EventRegistration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'location')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date')
    list_filter = ('event', 'registration_date')
    search_fields = ('user__username', 'user__email', 'event__title')
    date_hierarchy = 'registration_date'

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event', 'upload_date')
    list_filter = ('category', 'event', 'upload_date')
    search_fields = ('title', 'description', 'event__title', 'category__name')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'created_at')
    list_filter = ('event', 'rating', 'created_at')
    search_fields = ('user__username', 'event__title', 'content')
    date_hierarchy = 'created_at'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submission_date', 'is_resolved')
    list_filter = ('is_resolved', 'submission_date')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'submission_date', 'user')
    date_hierarchy = 'submission_date'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'user')
        }),
        ('Message', {
            'fields': ('message', 'submission_date')
        }),
        ('Response', {
            'fields': ('is_resolved', 'response', 'resolved_by', 'resolved_date')
        }),
    )
