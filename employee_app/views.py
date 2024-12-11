from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Login, Employee

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'admin123'

def login_view(request):
    if request.method == 'POST':
        # Get the credentials from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            request.session['username'] = username  
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login details')
    
    return render(request, 'employee_app/login.html')

# Dashboard View
def dashboard(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'employee_app/dashboard.html')

# Employee List
def employee_list(request):
    if 'username' not in request.session:
        return redirect('login')
    employees = Employee.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(f_Name__icontains=search_query)
    return render(request, 'employee_app/employee_list.html', {'employees': employees})

# Create Employee
from django.core.exceptions import ValidationError
from django.db import IntegrityError

def create_employee(request):
    if 'username' not in request.session:
        return redirect('login')

    if request.method == "POST":
        try:
            # Extracting the form data
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            designation = request.POST['designation']
            gender = request.POST['gender']
            course = request.POST['course']
            image = request.FILES.get('image')

            if not all([name, email, mobile, designation, gender, course, image]):
                raise ValidationError("All fields are required")

            # Create new employee record
            Employee.objects.create(
                f_Name=name, f_Email=email, f_Mobile=mobile, 
                f_Designation=designation, f_Gender=gender, 
                f_Course=course, f_Image=image
            )
            messages.success(request, 'Employee created successfully')
            return redirect('employee_list')

        except ValidationError as e:
            # Catching form validation errors
            messages.error(request, f'Validation Error: {str(e)}')
        
        except IntegrityError as e:
            # Catching database integrity errors (e.g., duplicate entries)
            messages.error(request, 'User with this data already exist')

        except Exception as e:
            # Catching any other unexpected error
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    
    return render(request, 'employee_app/create_employee.html')

# Edit Employee

def edit_employee(request, employee_id):
    if 'username' not in request.session:
        return redirect('login')

    employee = get_object_or_404(Employee, f_Id=employee_id)

    if request.method == "POST":
        try:
            # Extracting form data
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            designation = request.POST['designation']
            gender = request.POST['gender']
            # Get selected courses (checkboxes)
            courses = request.POST.getlist('course')
            image = request.FILES.get('image', employee.f_Image)  # Default to the current image if no new image

            # Check if all fields are filled out correctly
            if not all([name, email, mobile, designation, gender, courses]):
                raise ValidationError("All fields are required")

            # Update the employee record
            employee.f_Name = name
            employee.f_Email = email
            employee.f_Mobile = mobile
            employee.f_Designation = designation
            employee.f_Gender = gender
            employee.f_Course = ", ".join(courses)
            employee.f_Image = image
            employee.save()

            messages.success(request, 'Employee updated successfully')
            return redirect('employee_list')

        except ValidationError as e:
            messages.error(request, f'Validation Error: {str(e)}')
        
        except IntegrityError as e:
            messages.error(request, 'User with this data already exists')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'employee_app/edit_employee.html', {'employee': employee})
# Delete Employee
def delete_employee(request, employee_id):
    if 'username' not in request.session:
        return redirect('login')
    employee = get_object_or_404(Employee, f_Id=employee_id)
    employee.delete()
    messages.success(request, 'Employee deleted successfully')
    return redirect('employee_list')

# Logout
def logout_view(request):
    request.session.flush()
    return redirect('login')
