# Generated by Django 5.1.2 on 2024-10-26 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('pin_code', models.CharField(max_length=6)),
                ('industry', models.CharField(choices=[('IT & Services', 'IT & Services'), ('Trading', 'Trading'), ('Food production', 'Food production'), ('Airlines', 'Airlines'), ('Entertainment', 'Entertainment'), ('Engineering & Construction', 'Engineering & Construction'), ('Other', 'Other')], max_length=100)),
                ('company_type', models.CharField(blank=True, choices=[('Corporate', 'Corporate'), ('Foreign MNC', 'Foreign MNC'), ('Indian MNC', 'Indian MNC'), ('Startup', 'Startup'), ('Others', 'Others')], max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=100)),
                ('user', models.ForeignKey(limit_choices_to={'is_company': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('education_qualifications', models.TextField(blank=True, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cvs/')),
                ('college_name', models.CharField(blank=True, max_length=100, null=True)),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('pass_out_year', models.IntegerField(blank=True, null=True)),
                ('is_Fresher', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('years_of_experience', models.IntegerField(blank=True, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('is_Experienced', models.BooleanField(default=False)),
                ('user', models.ForeignKey(limit_choices_to={'is_employee': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
