# Generated by Django 5.1.2 on 2024-10-26 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_company_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_no',
            new_name='phone_number',
        ),
    ]
