from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0003b_add_incexp_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incexpitemsv2',
            name='subcategory',
        ),
    ]
