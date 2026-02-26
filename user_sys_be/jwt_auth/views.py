# jwt_auth/views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .jwt_utils import generate_token


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.is_active:
            return Response({"error": "Account is deactivated"}, status=403)
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": list(user.groups.values_list("name", flat=True)) 
        }

        token = generate_token(payload)

        return Response({
            "message": "Login successful",
            "access_token": token
        }, status=200)