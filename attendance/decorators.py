from django.http import HttpResponseForbidden

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Admin access only")
        return view_func(request, *args, **kwargs)
    return wrapper

