from functools import wraps
from django.http import JsonResponse

def login_required_api(view_func): #gets the function to be called
    @wraps(view_func)
    def wrapper(request, *args, **kwargs): #gets the request model
        if "user_email" not in request.session:
            return JsonResponse(
                {"error": "Authentication required"},
                status=401
            )
        return view_func(request, *args, **kwargs)
    return wrapper

def role_required_api(allowed_role): #gets the parameter passed
    def decorator(view_func): #gets the function to be called
        @wraps(view_func) # so that the function name is not lost
        def wrapper(request, *args, **kwargs): #gets the request model
            if request.session.get("role") != allowed_role:
                return JsonResponse(
                    {"error": "Unauthorized Role"},
                    status=403
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator