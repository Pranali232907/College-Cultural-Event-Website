from django.db import migrations

def update_media_categories(apps, schema_editor):
    MediaCategory = apps.get_model('events', 'MediaCategory')
    
    # Delete all existing categories
    MediaCategory.objects.all().delete()
    
    # Create new categories from model choices
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
        MediaCategory.objects.create(name=code)

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0007_populate_media_categories'),
    ]

    operations = [
        migrations.RunPython(update_media_categories),
    ]
