from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser) :
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    is_company = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['username', 'name', 'phone_number']

    def __str__(self):
        return self.username

class Company(models.Model) :
    INDUSTRY_CHOICES = [
        ('IT & Services', 'IT & Services'),
        ('Trading', 'Trading'),
        ('Food production', 'Food production'),
        ('Airlines', 'Airlines'),
        ('Entertainment', 'Entertainment'),
        ('Engineering & Construction', 'Engineering & Construction'),
        ('Other', 'Other'),
    ]

    TYPE_CHOICES = [
        ('Corporate', 'Corporate'),
        ('Foreign MNC', 'Foreign MNC'),
        ('Indian MNC', 'Indian MNC'),
        ('Startup', 'Startup'),
        ('Others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_company": True})
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=6)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    company_type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=True, null=True)
    # website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name
    
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=({"is_employee":True}))
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    education_qualifications = models.TextField(blank=True, null=True)
    
    # Fresher specific fields
    college_name = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    pass_out_year = models.IntegerField(blank=True, null=True)
    is_Fresher = models.BooleanField(default=False)
    
    # Experienced specific fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    is_Experienced = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name