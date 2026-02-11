from django.http import JsonResponse

def login_required_api(view_func):
    def wrapper(request, *args, **kwargs):
        if "user_email" not in request.session:
            return JsonResponse(
                {"error": "Authentication required"},
                status=401
            )
        return view_func(request, *args, **kwargs)
    return wrapper
