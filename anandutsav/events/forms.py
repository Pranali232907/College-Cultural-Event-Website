from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, Review, Contact, EventRegistration, Media, MediaCategory
from django.utils import timezone

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'mobile', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            user.first_name = self.cleaned_data['name']
            user.last_name = self.cleaned_data['mobile']  # Temporarily store mobile in last_name
            user.save()
        
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput())

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'location', 'rules']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'image', 'event']

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Very Good'),
        (3, '3 - Good'),
        (2, '2 - Fair'),
        (1, '1 - Poor')
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Share your experience about this event...'
        })
    )
    
    class Meta:
        model = Review
        fields = ['content', 'rating']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event']
        widgets = {
            'event': forms.HiddenInput()
        }

class ContactResponseForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 4})
        }

class MediaUploadForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter media title'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter media description'
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    category = forms.ModelChoiceField(
        queryset=MediaCategory.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=False,
        empty_label="Select an event (optional)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Media
        fields = ['title', 'description', 'image', 'category', 'event']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the event queryset to show only future events
        self.fields['event'].queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date') 