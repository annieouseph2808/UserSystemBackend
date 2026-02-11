from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .decorators import login_required_api,role_required_api


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error":"Only POST method allowed"},status=405)
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not email or not password or not role:
            return JsonResponse({"error":"Email, password and role are mandatory"},status=400)
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid email"},
                status=404
            )
        if not check_password(password, user.password):
            return JsonResponse(
                {"error": "Invalid password"},
                status=404
            )
        request.session["user_email"] = user.email
        request.session["role"] = user.role

        return JsonResponse({
            "message": "Login successful",
            "user_id": user.id,
            "role": user.role
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error":"Invalid JSON"},status=400)
    

@csrf_exempt
@login_required_api
@role_required_api("superadmin")
def add_user(request):
    if request.method != "POST":
        return JsonResponse({"error":"Only POST method allowed"},status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if User.objects.filter(email=email, is_active = True).exists():
            return JsonResponse(
                {"error": "User already exists"},
                status=409
            )
        User.objects.create(
            email=email,
            password=make_password(password),
            role=role
        )
        return JsonResponse(
            {"message": "User created successfully"},
            status=201
        )
        
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

@csrf_exempt
@login_required_api
@role_required_api("superadmin")
def delete_user(request):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Only DELETE method allowed"},
            status=405
        )
    try:
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse(
                {"error": "Email is required"},
                status=400
            )

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User does not exist"},
                status=404
            )

        user.is_active = False
        user.save()

        return JsonResponse(
            {"message": "User deactivated successfully"},
            status=200
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

@csrf_exempt
@login_required_api
def reactivate_user(request):
    if "user_email" not in request.session:
        return JsonResponse({"error":"Authentication Required"},statua=401)
    if request.method != "PUT":
        return JsonResponse(
            {"error": "Only PUT method allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse(
                {"error": "Email is required"},
                status=400
            )

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Deactivated User does not exist"},
                status=404
            )

        user.is_active = True
        user.save()

        return JsonResponse(
            {"message": "User activated successfully"},
            status=200
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
    

@csrf_exempt
@login_required_api
def view_users(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only DELETE method allowed"},
            status=405
        )
    users = User.objects.filter(is_active=True)
    if not users.exists():
        return JsonResponse(
            {"error": "No active users found"},
            status=404
        )
    data = [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]
    return JsonResponse({"users":data},status=200)



@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    if "user_email" not in request.session:
        return JsonResponse(
            {"error": "User not logged in"},
            status=401
        )

    request.session.flush() 

    return JsonResponse(
        {"message": "Logout successful"},
        status=200
    )