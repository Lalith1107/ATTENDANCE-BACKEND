from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import StaffProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

        login(request, user)

        # 🔑 ADMIN → Django Admin
        if user.is_superuser:
            return redirect('/admin/')

        # 👷 STAFF → Staff dashboard
        try:
            StaffProfile.objects.get(user=user)
            return redirect('/accounts/staff/dashboard/')
        except StaffProfile.DoesNotExist:
            messages.error(request, 'Staff profile not found')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required
def staff_dashboard(request):
    try:
        profile = StaffProfile.objects.get(user=request.user)
    except StaffProfile.DoesNotExist:
        messages.error(request, "Staff profile not found")
        return redirect('login')

    if profile.staff_category == 'SECURITY':
        return render(request, 'accounts/security_dashboard.html')

    elif profile.staff_category == 'HOUSEKEEPING':
        return render(request, 'accounts/housekeeping_dashboard.html')

    elif profile.staff_category == 'CANTEEN':
        return render(request, 'accounts/canteen_dashboard.html')

    else:
        return render(request, 'accounts/staff_dashboard.html')

