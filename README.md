# 🔐 auth_serv

Microservicio de autenticación del sistema SanosYSalvos. Se encarga de validar credenciales de usuarios, generar tokens JWT y verificar la validez de tokens en cada solicitud protegida.

**Puerto:** `8001`

---

## Responsabilidades

- Recibir credenciales (email + contraseña) y autenticar al usuario
- Generar tokens JWT firmados con la clave secreta del sistema
- Validar tokens JWT entrantes y devolver la información del usuario autenticado
- Comunicarse con `usuarios_serv` para verificar las credenciales

---

## Flujo de autenticación

```
Frontend → BFF → auth_serv → usuarios_serv (verificar email/password)
                           ← devuelve datos del usuario
              ← genera JWT token
        ← retorna token al frontend
```

En cada solicitud protegida:

```
Frontend → BFF → mascotas_serv → auth_serv (validar token)
                               ← token válido + datos del usuario
```

---

## Endpoints

| Método | URL | Descripción |
|---|---|---|
| POST | `/api/auth/login-token/` | Login con email y contraseña, retorna JWT |
| POST | `/api/auth/validate-token/` | Valida un token JWT y retorna datos del usuario |

### POST `/api/auth/login-token/`

**Request:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña"
}
```

**Response exitoso (200):**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "rol": "Dueno",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response fallido (401):**
```json
{
  "detail": "Invalid credentials"
}
```

### POST `/api/auth/validate-token/`

**Request:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response exitoso (200):**
```json
{
  "valid": true,
  "user_id": 1,
  "email": "usuario@ejemplo.com",
  "rol": "Dueno"
}
```

**Response fallido (401):**
```json
{
  "valid": false,
  "error": "Token inválido"
}
```

---

## Tests

Los tests usan mocks para simular las respuestas del `usuarios_serv` sin necesidad de tenerlo corriendo.

- `test_login_success` — Login exitoso con credenciales válidas, verifica que retorna token JWT
- `test_login_failure_invalid_email` — Login falla cuando el email no existe (status 401)
- `test_login_failure_invalid_password` — Login falla cuando la contraseña es incorrecta (status 401)
- `test_validate_token_success` — Token JWT válido es aceptado correctamente (status 200)
- `test_validate_token_failure` — Token inválido es rechazado (status 401)

```bash
cd auth_serv
python manage.py test
```

---

## Levantar el servicio

```bash
cd auth_serv
python manage.py migrate
python manage.py runserver 8001
```

> **Nota:** Requiere que `usuarios_serv` esté corriendo en el puerto 8000 para el flujo de login.
