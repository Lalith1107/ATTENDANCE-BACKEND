from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import StaffProfile
from django.shortcuts import render

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')  # Create this template later


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Admin user bypasses StaffProfile check
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('/admin/')  # Admin dashboard

            # Staff users must have StaffProfile
            staff_profile = getattr(user, 'staffprofile', None)
            if not staff_profile:
                return render(request, 'accounts/login.html', {'error': 'Staff profile not found'})
            
            if not staff_profile.is_active_staff:
                return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
            
            login(request, user)

            # Role-based redirect
            if staff_profile.staff_category == 'SECURITY':
                return redirect('/security/dashboard/')
            elif staff_profile.staff_category == 'HOUSEKEEPING':
                return redirect('/housekeeping/dashboard/')
            elif staff_profile.staff_category == 'CANTEEN':
                return redirect('/canteen/dashboard/')
            
            # Default staff dashboard
            return redirect('staff_dashboard')
        
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')
