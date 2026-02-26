from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from jwt_auth.decorators import JWTAuthGeneric
from .permissions import IsSuperAdminRole


class UsersView(JWTAuthGeneric, APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        if not users.exists():
            return Response({"error": "No active users found"}, status=404)

        data = [
            {
                "id": user.id,
                "username": user.username,
                "role": [group.name for group in user.groups.all()]
            }
            for user in users
        ]
        return Response({"users": data}, status=200)

    def post(self, request):
        # only super admin can create users
        # check role from jwt payload
        if not IsSuperAdminRole().has_permission(request):
            return Response({"error": "Permission denied"}, status=403)

        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        if not username or not password or not role:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username, is_active=True).exists():
            return Response({"error": "User already exists"}, status=409)

        try:
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            return Response({"error": "Invalid role"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=make_password(password)
        )
        user.groups.add(group)

        return Response({"message": "User created successfully"}, status=201)


class UserDetailView(JWTAuthGeneric, APIView):
    def _check_admin(self, request):
        return IsSuperAdminRole().has_permission(request)



    def delete(self, request, username):
        if not self._check_admin(request): #only if user is superadmin
            return Response({"error": "Permission denied"}, status=403)
        try:
            user = User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        user.delete()
        return Response({"message": "User deactivated successfully"}, status=200)



    def put(self, request, username):
        if not self._check_admin(request):
            return Response({"error": "Permission denied"}, status=403)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        new_username = request.data.get("username")
        new_password = request.data.get("password")
        new_role = request.data.get("role")
        if not new_username or not new_password or not new_role:
            return Response(
                {"error": "PUT requires all fields: username, password, role"},
                status=400
            )
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            return Response({"error": "Username already taken"}, status=409)
        try:
            group = Group.objects.get(name=new_role)
        except Group.DoesNotExist:
            return Response({"error": "Invalid role"}, status=400)
        user.username = new_username
        user.set_password(new_password)
        user.groups.clear()
        user.groups.add(group)
        user.save()
        return Response({
            "message": "User updated successfully",
            "user": {
                "username": user.username,
                "role": new_role
            }
        }, status=200)
    


    def patch(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        new_username = request.data.get("username")
        new_password = request.data.get("password")
        new_role = request.data.get("role")

        if new_username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return Response({"error": "Username already taken"}, status=409)
            user.username = new_username

        if new_password:
            user.set_password(new_password) 

        if new_role:
            try:
                group = Group.objects.get(name=new_role)
            except Group.DoesNotExist:
                return Response({"error": "Invalid role"}, status=400)
            user.groups.clear()  
            user.groups.add(group) 

        user.save()

        return Response({
            "message": "User updated successfully",
            "updated_fields": {
                "username": new_username or "unchanged",
                "password": "updated" if new_password else "unchanged",
                "role": new_role or "unchanged"
            }
        }, status=200)