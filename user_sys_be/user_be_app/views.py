from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdminRole,IsUserRole  
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsSuperAdminRole])
def add_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")
    if not username or not password or not role:
        return Response({"error": "All fields required"}, status=400)#400 as it is a client issue
    
    if User.objects.filter(username=username, is_active = True).exists():
        return JsonResponse(
            {"error": "User already exists"},
            status=409 #conflict
        )
    try:
        group = Group.objects.get(name=role)
    except Group.DoesNotExist:
        return Response({"error": "Invalid role"}, status=400) #client request issue so 400
    
    user = User.objects.create_user(
        username=username,
        password=make_password(password)
    )
    user.groups.add(group)
    return JsonResponse(
        {"message": "User created successfully"},
        status=201
    )

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsSuperAdminRole])
def delete_user(request):
    username = request.data.get("username")
    if not username:
        return JsonResponse(
            {"error": "username is required"},
            status=400
        )
    try:
        user = User.objects.get(username=username, is_active=True)
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


@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsSuperAdminRole])
def reactivate_user(request):
    username = request.data.get("username")
    if not username:
        return JsonResponse(
            {"error": "username is required"},
            status=400
        )

    try:
        user = User.objects.get(username=username, is_active=False)
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
    

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_users(request):
    users = User.objects.filter(is_active=True)
    if not users.exists():
        return JsonResponse(
            {"error": "No active users found"},
            status=404
        )
    data = [
        {
            "id": user.id,
            "username": user.username,
            "role": user.is_superuser
        }
        for user in users
    ]
    return JsonResponse({"users":data},status=200)
