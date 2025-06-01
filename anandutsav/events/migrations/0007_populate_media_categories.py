from django.db import migrations

def populate_media_categories(apps, schema_editor):
    MediaCategory = apps.get_model('events', 'MediaCategory')
    
    categories = [
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
    
    for code, name in categories:
        MediaCategory.objects.get_or_create(
            name=code,
            defaults={'description': f"Media related to {name} events"}
        )

def reverse_populate(apps, schema_editor):
    MediaCategory = apps.get_model('events', 'MediaCategory')
    MediaCategory.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0006_merge_20250325_1409'),
    ]

    operations = [
        migrations.RunPython(
            populate_media_categories,
            reverse_code=reverse_populate
        ),
    ]
