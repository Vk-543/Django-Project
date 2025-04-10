from django.db import migrations, models
from django.utils import timezone

def set_default_show_time(apps, schema_editor):
    Booking = apps.get_model('movies', 'Booking')
    # Set a default show time for existing bookings
    Booking.objects.filter(show_time__isnull=True).update(show_time=timezone.now())

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_add_show_time_with_default'),
    ]

    operations = [
        migrations.RunPython(set_default_show_time),
    ]
