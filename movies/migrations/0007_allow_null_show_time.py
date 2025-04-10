from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_set_default_show_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='show_time',
            field=models.DateTimeField(null=True),
        ),
    ]
