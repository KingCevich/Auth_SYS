from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt, time
from django.conf import settings
import requests
import datetime

@api_view(["POST"])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # Llamada al microservicio Usuarios
    usuarios_url = "http://127.0.0.1:8000/api/usuarios/"
    response = requests.get(usuarios_url, params={"email": email})

    if response.status_code != 200 or not response.json():
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    user_data = response.json()[0]  # suponiendo que devuelve lista de usuarios

    # Validar contraseña encriptada
    if not check_password(password, user_data["password"]):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generar token
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "rol": user_data["rol"],
        "iat": int(time.time()),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        "id": user_data["id"],
        "email": user_data["email"],
        "rol": user_data["rol"],
        "token": token
    }, status=status.HTTP_200_OK)