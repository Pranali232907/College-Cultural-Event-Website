from django.db import migrations

def add_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('events', 'EventCategory')
    
    categories = [
        {
            'name': 'Performing Events',
            'description': 'Dance, music, drama, and other stage performances that showcase artistic talent.'
        },
        {
            'name': 'Fine Art Events',
            'description': 'Painting, sculpture, sketching, and other visual arts that express creativity.'
        },
        {
            'name': 'Media Events',
            'description': 'Photography, filmmaking, digital art, and other media-based creative expressions.'
        },
        {
            'name': 'General Events',
            'description': 'Workshops, competitions, exhibitions, and other general cultural activities.'
        }
    ]
    
    for category in categories:
        EventCategory.objects.get_or_create(
            name=category['name'],
            defaults={'description': category['description']}
        )

def remove_event_categories(apps, schema_editor):
    EventCategory = apps.get_model('events', 'EventCategory')
    EventCategory.objects.filter(name__in=[
        'Performing Events',
        'Fine Art Events',
        'Media Events',
        'General Events'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(add_event_categories, remove_event_categories),
    ] 