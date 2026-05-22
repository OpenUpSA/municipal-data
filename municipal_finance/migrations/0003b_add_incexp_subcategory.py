from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0005_auto_20240814_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='incexpitemsv2',
            name='subcategory',
            field=models.TextField(blank=True, null=True),
        ),
    ]
