from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),  # Change this to the first migration

    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='show_time',
            field=models.DateTimeField(),
        ),
    ]
