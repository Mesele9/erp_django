# common_user/middleware.py
from django.shortcuts import redirect

class RoleBasedRedirectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.path == '/':
            if request.user.role =='hr_staff':
                return redirect('hr_dashboard')
            elif request.user.role =='store_staff':
                return redirect('store_dashboard')
            elif request.user.role == 'reception':
                return redirect('upload_dashboard')
            elif request.user.is_superuser or request.user.role == 'admin':
                return redirect('admin_dashboard')
        return response
