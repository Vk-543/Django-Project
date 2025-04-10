from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime.now),  # Set a default value
        ),
    ]
