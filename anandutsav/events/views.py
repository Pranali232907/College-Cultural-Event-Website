from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Event, EventCategory, Media, Review, Contact, EventRegistration, MediaCategory
from .forms import (
    UserRegisterForm, UserLoginForm, EventForm, 
    ReviewForm, ContactForm, EventRegistrationForm, 
    ContactResponseForm, MediaUploadForm
)

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Home views
def home(request):
    # Get featured events
    events = Event.objects.order_by('-date')[:4]
    # Get featured media
    media = Media.objects.order_by('-upload_date')[:4]
    # Get recent reviews
    reviews = Review.objects.order_by('-created_at')[:3]
    # Get all media categories
    media_categories = MediaCategory.objects.all()
    
    return render(request, 'events/home.html', {
        'events': events,
        'media': media,
        'reviews': reviews,
        'media_categories': media_categories,
    })

def about(request):
    return render(request, 'events/about.html')

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome, {user.username}!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    
    return render(request, 'events/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'events/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully!')
    return redirect('home')

# Event views
def event_list(request):
    categories = EventCategory.objects.all()
    selected_category = request.GET.get('category')
    
    # Handle both slug-based and ID-based category filtering
    if selected_category:
        if selected_category.isdigit():
            events = Event.objects.filter(category__id=selected_category).order_by('-date')
        else:
            # Map category slugs to names
            category_map = {
                'performing': 'Performing Events',
                'fine-art': 'Fine Art Events',
                'media': 'Media Events',
                'general': 'General Events'
            }
            category_name = category_map.get(selected_category)
            if category_name:
                events = Event.objects.filter(category__name=category_name).order_by('-date')
            else:
                events = Event.objects.all().order_by('-date')
    else:
        events = Event.objects.all().order_by('-date')
    
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration_form = EventRegistrationForm(initial={'event': event})
    review_form = ReviewForm()
    
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    
    reviews = Review.objects.filter(event=event).order_by('-created_at')
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'registration_form': registration_form,
        'review_form': review_form,
        'reviews': reviews,
    })

@login_required
def register_for_event(request, event_id):
    # Prevent admin users from registering
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot register for events.')
        return redirect('event_detail', event_id=event_id)
        
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            # Check if already registered
            if EventRegistration.objects.filter(user=request.user, event=event).exists():
                messages.warning(request, 'You are already registered for this event!')
            else:
                registration = form.save(commit=False)
                registration.user = request.user
                registration.event = event
                registration.save()
                messages.success(request, f'Successfully registered for {event.title}!')
            
            return redirect('event_detail', event_id=event.id)
    
    return redirect('event_detail', event_id=event.id)

# Admin views for events
@user_passes_test(is_admin)
def admin_event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/admin_event_list.html', {'events': events})

@user_passes_test(is_admin)
def admin_event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('admin_event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/admin_event_form.html', {
        'form': form,
        'action': 'Create'
    })

@user_passes_test(is_admin)
def admin_event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_event_list')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/admin_event_form.html', {
        'form': form,
        'event': event,
        'action': 'Update'
    })

@user_passes_test(is_admin)
def admin_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_event_list')
    
    return render(request, 'events/admin_event_confirm_delete.html', {
        'event': event
    })

# Media views
def media_list(request):
    selected_category = request.GET.get('category')
    media_categories = MediaCategory.objects.all()
    
    if selected_category:
        media = Media.objects.filter(category__name=selected_category).order_by('-upload_date')
    else:
        media = Media.objects.all().order_by('-upload_date')
        
    return render(request, 'events/media_list.html', {
        'media': media,
        'media_categories': media_categories
    })

def media_detail(request, media_id):
    media_item = get_object_or_404(Media, id=media_id)
    related_media = Media.objects.filter(event=media_item.event).exclude(id=media_id)[:4]
    
    return render(request, 'events/media_detail.html', {
        'media': media_item,
        'related_media': related_media,
    })

# Admin Media views
@user_passes_test(is_admin)
def admin_media_list(request):
    media = Media.objects.all().order_by('-upload_date')
    return render(request, 'events/admin_media_list.html', {
        'media': media
    })

@user_passes_test(is_admin)
def admin_media_upload(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('admin_media_list')
    else:
        form = MediaUploadForm()
    
    # Get all events for the dropdown
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    return render(request, 'events/admin_media_upload.html', {
        'form': form,
        'events': events
    })

@user_passes_test(is_admin)
def admin_media_delete(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Media deleted successfully!')
    return redirect('admin_media_list')

# Review views
@login_required
def add_review(request, event_id):
    # Prevent admin users from adding reviews
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot submit reviews.')
        return redirect('event_detail', event_id=event_id)
        
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('event_detail', event_id=event.id)
    
    return redirect('event_detail', event_id=event.id)

# Admin Review views
@user_passes_test(is_admin)
def admin_review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'events/admin_review_list.html', {
        'reviews': reviews
    })

@user_passes_test(is_admin)
def admin_review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
    return redirect('admin_review_list')

# Contact views
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            messages.success(request, 'Your message has been sent! We will get back to you soon.')
            return redirect('contact')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.first_name,
                'email': request.user.email,
                'phone': request.user.last_name,  # Temporarily using last_name for phone
            }
        form = ContactForm(initial=initial_data)
    
    return render(request, 'events/contact.html', {'form': form})

# Admin Contact views
@user_passes_test(is_admin)
def admin_contact_list(request):
    contacts = Contact.objects.all().order_by('-submission_date')
    return render(request, 'events/admin_contact_list.html', {
        'contacts': contacts
    })

@user_passes_test(is_admin)
def admin_contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        form = ContactResponseForm(request.POST)
        if form.is_valid():
            contact.response = form.cleaned_data['response']
            contact.resolved = True
            contact.resolved_by = request.user
            contact.resolution_date = timezone.now()
            contact.save()
            messages.success(request, 'Response sent successfully!')
            return redirect('admin_contact_list')
    
    return render(request, 'events/admin_contact_detail.html', {
        'contact': contact
    })

@login_required
def my_registrations(request):
    # Prevent admin access
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot access registration history.')
        return redirect('home')
    
    registrations = EventRegistration.objects.filter(user=request.user).order_by('-registration_date')
    return render(request, 'events/my_registrations.html', {
        'registrations': registrations
    })

@login_required
def my_reviews(request):
    # Prevent admin access
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot access review history.')
        return redirect('home')
    
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'events/my_reviews.html', {
        'reviews': reviews
    })

@login_required
def delete_review(request, review_id):
    # Prevent admin access
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot delete reviews from this interface.')
        return redirect('home')
    
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        event_id = review.event.id
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('event_detail', event_id=event_id)
    return render(request, 'events/delete_review.html', {'review': review})

@login_required
def cancel_registration(request, registration_id):
    # Prevent admin access
    if request.user.is_staff:
        messages.warning(request, 'Admin users cannot cancel registrations from this interface.')
        return redirect('home')
    
    registration = get_object_or_404(EventRegistration, id=registration_id, user=request.user)
    if request.method == 'POST':
        event_id = registration.event.id
        registration.delete()
        messages.success(request, 'Your registration has been cancelled.')
        return redirect('event_detail', event_id=event_id)
    return render(request, 'events/cancel_registration.html', {'registration': registration})

# Admin views for registrations
@user_passes_test(is_admin)
def admin_registrations(request):
    registrations = EventRegistration.objects.all().order_by('-registration_date')
    return render(request, 'events/admin_registrations.html', {
        'registrations': registrations
    })

@user_passes_test(is_admin)
def admin_registration_delete(request, registration_id):
    registration = get_object_or_404(EventRegistration, id=registration_id)
    if request.method == 'POST':
        registration.delete()
        messages.success(request, 'Registration deleted successfully!')
    return redirect('admin_registrations')
