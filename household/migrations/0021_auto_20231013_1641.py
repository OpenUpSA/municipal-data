# Generated by Django 2.2.28 on 2023-10-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0020_remove_financialyear_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='householdbilltotal',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='householdservicetotal',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]
