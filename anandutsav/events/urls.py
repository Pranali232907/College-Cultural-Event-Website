from django.urls import path, include
from . import views

urlpatterns = [
    # Home and general pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Authentication
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    
    # User Dashboard
    path('my/registrations/', views.my_registrations, name='my_registrations'),
    path('my/reviews/', views.my_reviews, name='my_reviews'),
    path('my/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('my/registrations/<int:registration_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    
    # Reviews
    path('events/<int:event_id>/review/', views.add_review, name='add_review'),
    
    # Media
    path('media/', views.media_list, name='media_list'),
    path('media/<int:media_id>/', views.media_detail, name='media_detail'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Custom Admin Management
    path('manage/events/', views.admin_event_list, name='admin_event_list'),
    path('manage/events/create/', views.admin_event_create, name='admin_event_create'),
    path('manage/events/<int:event_id>/update/', views.admin_event_update, name='admin_event_update'),
    path('manage/events/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),
    
    path('manage/media/', views.admin_media_list, name='admin_media_list'),
    path('manage/media/upload/', views.admin_media_upload, name='admin_media_upload'),
    path('manage/media/<int:media_id>/delete/', views.admin_media_delete, name='admin_media_delete'),
    
    path('manage/registrations/', views.admin_registrations, name='admin_registrations'),
    path('manage/registrations/<int:registration_id>/delete/', views.admin_registration_delete, name='admin_registration_delete'),
    
    path('manage/reviews/', views.admin_review_list, name='admin_review_list'),
    path('manage/reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    
    path('manage/contacts/', views.admin_contact_list, name='admin_contact_list'),
    path('manage/contacts/<int:contact_id>/', views.admin_contact_detail, name='admin_contact_detail'),
]
