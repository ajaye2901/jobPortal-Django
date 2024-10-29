import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import*
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from jobapp.models import *
from django.conf import settings
from django.db import transaction
# Create your views here.

def register_company(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            pin_code = request.POST.get('pin_code')
            industry = request.POST.get('industry')
            location = request.POST.get('location')  # Extract location data
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            # website = request.POST.get('website')  # Optional field
            description = request.POST.get('description')  # Optional field

            # Validate data
            if not all([name, email, phone_number, address , pin_code,  industry, location, password, confirm_password]):
                messages.error(request, 'All fields are required.')
                return render(request, 'register_company.html')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'register_company.html')

            # Check if username already exists
            User = get_user_model()
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'register_company.html')

            # Create a new User instance
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password,
                name=name,
                phone_number=phone_number,
                is_company=True
            )

            # Create a new Company instance linked to the User
            company = Company.objects.create(
                user=user,
                address=address,
                pin_code=pin_code,
                industry=industry,
                location=location,  # Include location in the company creation
                # website=website,
                description=description,
                name=name  # Ensure this field is included
            )

            # Success message and redirect
            messages.success(request, 'Company registered successfully.')
            return redirect('login_company')  # Replace with your URL name for the success page

        except KeyError as e:
            # Handle missing POST data
            messages.error(request, f'Missing field: {e.args[0]}')
            return render(request, 'register_company.html')
        except IntegrityError as e:
            # Handle integrity errors (e.g., unique constraints)
            messages.error(request, str(e))
            return render(request, 'register_company.html')
        except Exception as e:
            # Handle other exceptions
            messages.error(request, str(e))
            return render(request, 'register_company.html')

    # Render a registration form (GET request)
    return render(request, 'register_company.html')

def user_register(request):
    if request.method == 'POST':
        # Extract data from POST request
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        password = request.POST['password']
        education_qualifications = request.POST['education_qualifications']
        university = request.POST['university']
        pass_out_year = request.POST['pass_out_year']
        date_of_birth = request.POST['date_of_birth']
        company_name = request.POST['company_name']
        years_of_experience = request.POST['years_of_experience']
        designation = request.POST['designation']
        user_type = request.POST['user_type']

        try:
            User = get_user_model()
            user = User.objects.create_user(username=name, email=email, password=password, phone_number=phone_number, is_employee=True)

            # Determine user type and set corresponding attributes
            if user_type == 'fresher':
                college_name = request.POST['college_name']
                university = request.POST['university']
                pass_out_year = request.POST['pass_out_year']

                # Create a new Employee instance for fresher
                new_user = Employee.objects.create(
                    user=user,
                    gender=gender,
                    college_name=college_name,
                    university=university,
                    pass_out_year=pass_out_year,
                    date_of_birth=date_of_birth,
                    education_qualifications=education_qualifications,
                    is_Fresher=True
                )

            elif user_type == 'experienced':
                company_name = request.POST['company_name']
                years_of_experience = request.POST['years_of_experience']
                designation = request.POST['designation']

                # Create a new Employee instance for experienced user
                new_user = Employee.objects.create(
                    user=user,
                    gender=gender,
                    company_name=company_name,
                    years_of_experience=years_of_experience,
                    designation=designation,
                    date_of_birth=date_of_birth,
                    education_qualifications=education_qualifications,
                    is_Experienced=True
                )

            # Save the new user
            new_user.save()

            # Authenticate and login the user
            messages.success(request, 'User registered successfully.')
            return redirect('user_login')

        except Exception as e:
            # Handle the error gracefully, maybe render the registration form again with error messages
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'user_register.html')

    # Render a registration form (GET request)
    return render(request, 'user_register.html')
  

def login_company(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, 'No company profile found. Please create one first.')
            return redirect('register_company')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successful')
                return redirect('company_dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'login_company.html')

    return render(request, 'login_company.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, 'email does not exist.')
            return render(request, 'user_login.html')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'user_login.html')
    
    return render(request, 'user_login.html')

def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, 'No company profile found. Please create one first.')
            return redirect('register_company')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None and authenticated_user.is_superuser:
                login(request, authenticated_user)
                messages.success(request, 'Login Successful')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'admin_login.html')

    return render(request, 'admin_login.html')

def mainlogin(request):
    return render(request, 'mainlogin.html' )    

def user_dashboard(request):
    if request.user.is_authenticated and request.user.is_employee:
        try:
            current_user = Employee.objects.get(user=request.user)
            jobs = Job.objects.all() 
        except Employee.DoesNotExist:
            current_user = None
            jobs = Job.objects.all()
    else:
        return redirect('user_login')
    return render(request, 'user_dashboard.html',{'employee' :current_user ,'jobs': jobs} )   

def company_dashboard(request):
    if request.user.is_authenticated and request.user.is_company:
        try:
            current_company = Company.objects.get(user=request.user)
            jobs = Job.objects.filter(company_name=current_company)
        except Company.DoesNotExist:
            current_company = None
            jobs = []
    else:
        return redirect('login_employee')  # Redirect if not a company user

    # Pass the company object to the template
    return render(request, 'dashboard.html', {'company': current_company, 'jobs': jobs})


def admin_dashboard(request):
    companies = Company.objects.all()
    employees = Employee.objects.all()  # Query all employees

    context = {
        'companies': companies,
        'employees': employees,
    }
    return render(request, 'admin_dashboard.html', context)

def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.user.username = request.POST.get('username', employee.user.username)
        employee.is_Fresher = 'is_Fresher' in request.POST
        employee.is_Experienced = 'is_Experienced' in request.POST
        employee.save()
        messages.success(request, 'User updated successfully.')
        return redirect('admin_dashboard')
    return render(request, 'edit_user.html', {'employee': employee})


def user_delete(request, employee_id):
    # Retrieve the employee based on the provided ID
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        try:
            # Retrieve the associated user
            user = employee.user
            username = user.username  # Store for message display
            
            # Delete the user, which will also remove the employee (if cascade is enabled)
            user.delete()
            
            # Success message
            messages.success(request, f'User "{username}" and associated employee deleted successfully.')
        except Exception as e:
            # Handle errors gracefully and display an error message
            messages.error(request, f'Error deleting user: {str(e)}')
        
        # Redirect to admin dashboard after deletion
        return redirect('admin_dashboard')
    
    # Render confirmation page
    return render(request, 'confirm_delete_user.html', {'employee': employee})



def view_company(request, id):
    company = get_object_or_404(Company, id=id)
    return render(request, 'view_company.html', {'company': company})


def edit_company(request, id):
    company = get_object_or_404(Company, id=id)
    
    if request.method == 'POST':
        company.address = request.POST.get('address')
        company.pin_code = request.POST.get('pin_code')
        company.industry = request.POST.get('industry')
        company.location = request.POST.get('location')  
        company.description = request.POST.get('description')
        company.save()
        messages.success(request, 'Company details updated successfully.')
        return redirect('view_company', id=company.id)

    return render(request, 'edit_company.html', {'company': company})


def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        try:
            user = company.user
            username = user.username

            user.delete()

            messages.success(request, f'User "{username}" and associated employee deleted successfully.')
        except Exception as e:
            # Handle errors gracefully and display an error message
            messages.error(request, f'Error deleting user: {str(e)}')
        
        # Redirect to admin dashboard after deletion
        return redirect('admin_dashboard')
    


def logout_company(request):
    logout(request)
    return redirect('index')  

def logout_employee(request):
    logout(request)
    return redirect('index')  


# Check if the user is a superuser
def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def logout_superuser(request):
    logout(request)
    return redirect('login_admin')  # Redirect to the login page or any other page