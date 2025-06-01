from django.db import migrations

def add_media_categories(apps, schema_editor):
    MediaCategory = apps.get_model('events', 'MediaCategory')
    
    categories = [
        {
            'name': 'Event Photos',
            'description': 'Photographs from various cultural events and performances.'
        },
        {
            'name': 'Artwork',
            'description': 'Artwork and creative pieces from fine arts events.'
        },
        {
            'name': 'Performance',
            'description': 'Images from dance, music, and drama performances.'
        },
        {
            'name': 'Workshops',
            'description': 'Photos from workshops and interactive sessions.'
        },
        {
            'name': 'Awards & Recognition',
            'description': 'Images from prize distribution and award ceremonies.'
        }
    ]
    
    for category in categories:
        MediaCategory.objects.get_or_create(
            name=category['name'],
            defaults={'description': category['description']}
        )

def remove_media_categories(apps, schema_editor):
    MediaCategory = apps.get_model('events', 'MediaCategory')
    MediaCategory.objects.filter(name__in=[
        'Event Photos',
        'Artwork',
        'Performance',
        'Workshops',
        'Awards & Recognition'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_create_media_category'),
    ]
    
    operations = [
        migrations.RunPython(add_media_categories, remove_media_categories),
    ] 