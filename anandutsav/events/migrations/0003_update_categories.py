from django.db import migrations

def update_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('events', 'EventCategory')
    
    # Update existing categories
    categories = [
        {
            'name': 'Performing Events',
            'description': 'Dance, music, drama, and other stage performances that showcase artistic talent.'
        },
        {
            'name': 'Fine Arts Events',
            'description': 'Painting, sculpture, sketching, and other visual arts that express creativity.'
        },
        {
            'name': 'Media Events',
            'description': 'Photography, filmmaking, digital art, and other media-based creative expressions.'
        },
        {
            'name': 'General Events',
            'description': 'Traditional and cultural activities, workshops, competitions, and exhibitions.'
        }
    ]
    
    # Delete existing categories
    EventCategory.objects.all().delete()
    
    # Create new categories
    for category in categories:
        EventCategory.objects.create(**category)

def remove_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('events', 'EventCategory')
    EventCategory.objects.filter(name__in=[
        'Performing Events',
        'Fine Arts Events',
        'Media Events',
        'General Events'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_add_event_categories'),
    ]
    
    operations = [
        migrations.RunPython(update_event_categories, remove_event_categories),
    ]