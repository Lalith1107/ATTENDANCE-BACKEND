from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import StaffProfile


# =========================
# STAFF DASHBOARDS
# =========================
@login_required
def staff_dashboard(request):
    return render(request, "accounts/staff_dashboard.html")


@login_required
def security_dashboard(request):
    return render(request, "accounts/security_dashboard.html")


@login_required
def housekeeping_dashboard(request):
    return render(request, "accounts/housekeeping_dashboard.html")


@login_required
def canteen_dashboard(request):
    return render(request, "accounts/canteen_dashboard.html")


# =========================
# LOGIN VIEW (FIXED)
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid username or password"}
            )

        # ✅ LOGIN USER
        login(request, user)

        # =========================
        # ADMIN (ONLY SUPERUSER)
        # =========================
        if user.is_superuser:
            return redirect("/admin/")

        # =========================
        # STAFF PROFILE CHECK
        # =========================
        try:
            staff_profile = StaffProfile.objects.get(user=user)
        except StaffProfile.DoesNotExist:
            return render(
                request,
                "accounts/login.html",
                {"error": "Staff profile not found. Contact admin."}
            )

        if not staff_profile.is_active_staff:
            return render(
                request,
                "accounts/login.html",
                {"error": "Your account is inactive"}
            )

        # =========================
        # ROLE-BASED REDIRECT
        # =========================
        if staff_profile.staff_category == "SECURITY":
            return redirect("security_dashboard")

        elif staff_profile.staff_category == "HOUSEKEEPING":
            return redirect("housekeeping_dashboard")

        elif staff_profile.staff_category == "CANTEEN":
            return redirect("canteen_dashboard")

        # =========================
        # DEFAULT STAFF DASHBOARD
        # =========================
        return redirect("staff_dashboard")

    return render(request, "accounts/login.html")
