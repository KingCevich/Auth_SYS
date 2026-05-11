from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import Client
from unittest.mock import patch, MagicMock


class AuthTests(APITestCase):
    # Tests del servicio de autenticación: login y validación de tokens JWT
    def setUp(self):
        self.client = Client()

    # Verifica que el login sea exitoso con credenciales válidas y retorna JWT token
    @patch('auth_app.views.requests.get')
    @patch('auth_app.views.check_password')
    def test_login_success(self, mock_check_password, mock_get):
        # Mock the response from usuarios_serv
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'id': 1,
            'email': 'test@example.com',
            'password': 'hashed_password',
            'rol': 'usuario'
        }]
        mock_get.return_value = mock_response
        mock_check_password.return_value = True

        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'testpass'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    # Verifica que el login falla con un email inválido (usuario no encontrado)
    @patch('auth_app.views.requests.get')
    def test_login_failure_invalid_email(self, mock_get):
        # Mock the response from usuarios_serv - no user found
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        url = reverse('login')
        data = {'email': 'invalid@example.com', 'password': 'testpass'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Verifica que el login falla cuando la contraseña es incorrecta
    @patch('auth_app.views.requests.get')
    @patch('auth_app.views.check_password')
    def test_login_failure_invalid_password(self, mock_check_password, mock_get):
        # Mock the response from usuarios_serv
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'id': 1,
            'email': 'test@example.com',
            'password': 'hashed_password',
            'rol': 'usuario'
        }]
        mock_get.return_value = mock_response
        mock_check_password.return_value = False  # Password check fails

        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'wrongpass'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Verifica que un token JWT válido sea aceptado en la validación
    def test_validate_token_success(self):
        # For validate_token, we need to create a valid token first
        import jwt
        from django.conf import settings
        import time

        payload = {
            "user_id": 1,
            "email": "test@example.com",
            "rol": "usuario",
            "iat": int(time.time()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        url = reverse('validate_token')
        data = {'token': token}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Verifica que un token inválido sea rechazado en la validación
    def test_validate_token_failure(self):
        url = reverse('validate_token')
        data = {'token': 'invalidtoken'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
