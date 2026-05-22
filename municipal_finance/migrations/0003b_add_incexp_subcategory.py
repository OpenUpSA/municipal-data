from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0003_add_item_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='incexpitemsv2',
            name='subcategory',
            field=models.TextField(blank=True, null=True),
        ),
    ]
