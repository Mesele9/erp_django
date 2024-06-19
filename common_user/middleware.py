# common_user/middleware.py
from django.shortcuts import redirect

class RoleBasedRedirectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.path == '/':
            if request.user.groups.filter(name='hr_staff').exists():
                return redirect('hr_dashboard')
            elif request.user.groups.filter(name='store_staff').exists():
                return redirect('store_dashboard')
            elif request.user.is_superuser:
                return redirect('admin_dashboard')
        return response
