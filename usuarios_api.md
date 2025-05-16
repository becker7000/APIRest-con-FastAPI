
---

## ✅ 1. `models/usuario.py` – Modelos Pydantic

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# Modelo base para los usuarios
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr  # Valida formato de email
    rol: Literal["admin", "empleado", "cliente"] = "cliente"  # Rol permitido

# Modelo para crear un usuario (registro)
class UsuarioCreate(UsuarioBase):
    password: str  # Contraseña cruda (se hashea luego)

# Modelo para login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Modelo para representar usuario almacenado (con hash de contraseña)
class UsuarioInDB(UsuarioBase):
    id: Optional[str]
    hashed_password: str  # Contraseña ya encriptada

# Modelo público (lo que se retorna al cliente)
class UsuarioPublico(UsuarioBase):
    id: str
```

---

## ✅ 2. `core/security.py` – Seguridad y JWT

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt  # Manejo de JWT

# Llave secreta para firmar tokens JWT (usa variable de entorno en producción)
SECRET_KEY = "supersecreto123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Tiempo de expiración

# Contexto de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashea una contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# Verifica si una contraseña concuerda con su hash
def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

# Crea un token JWT con tiempo de expiración
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decodifica y verifica un token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## ✅ 3. `database/collections.py` – Agrega esta línea si no existe

```python
usuarios_collection = db["usuarios"]  # Colección MongoDB para usuarios
```

---

## ✅ 4. `services/auth_service.py` – Registro y login

```python
from app.database.collections import usuarios_collection
from app.core.security import hash_password, verify_password, create_access_token
from app.models.usuario import UsuarioCreate, UsuarioLogin

# Función para registrar usuario
def registrar_usuario(usuario: UsuarioCreate):
    # Evita duplicación por email
    if usuarios_collection.find_one({"email": usuario.email}):
        return None
    # Crea documento con contraseña hasheada
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol,
        "hashed_password": hash_password(usuario.password)
    }
    # Guarda en base de datos
    res = usuarios_collection.insert_one(nuevo_usuario)
    return str(res.inserted_id)

# Función para login (autenticación)
def autenticar_usuario(login_data: UsuarioLogin):
    # Busca usuario por email
    usuario_db = usuarios_collection.find_one({"email": login_data.email})
    # Verifica existencia y contraseña
    if not usuario_db or not verify_password(login_data.password, usuario_db["hashed_password"]):
        return None
    # Crea token con ID y rol
    token = create_access_token({"sub": str(usuario_db["_id"]), "rol": usuario_db["rol"]})
    return token
```

---

## ✅ 5. `routes/auth.py` – Registro y login

```python
from fastapi import APIRouter, HTTPException
from app.models.usuario import UsuarioCreate, UsuarioLogin
from app.services.auth_service import registrar_usuario, autenticar_usuario

# Rutas relacionadas con autenticación
router = APIRouter(prefix="/auth", tags=["Auth"])

# Endpoint para registrar usuarios
@router.post("/register")
def register(usuario: UsuarioCreate):
    user_id = registrar_usuario(usuario)
    if not user_id:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return {"msg": "Usuario registrado correctamente", "id": user_id}

# Endpoint para login
@router.post("/login")
def login(datos: UsuarioLogin):
    token = autenticar_usuario(datos)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": token, "token_type": "bearer"}
```

---

## ✅ 6. `core/dependencies.py` – Middleware de seguridad

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.database.collections import usuarios_collection
from bson.objectid import ObjectId

# Extrae token JWT del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependencia que retorna el usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = usuarios_collection.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": str(user["_id"]), "email": user["email"], "rol": user["rol"]}

# Verifica que el usuario tenga uno de los roles requeridos
def require_role(roles: list):
    def role_checker(user=Depends(get_current_user)):
        if user["rol"] not in roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return user
    return role_checker
```

---

## ✅ 7. `routes/usuarios.py` – Listar usuarios (solo admin)

```python
from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.database.collections import usuarios_collection
from app.models.usuario import UsuarioPublico

# Rutas protegidas para administración de usuarios
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Devuelve todos los usuarios (solo para admins)
@router.get("/", response_model=list[UsuarioPublico])
def listar_usuarios(admin=Depends(require_role(["admin"]))):
    usuarios = []
    for u in usuarios_collection.find():
        usuarios.append({
            "id": str(u["_id"]),
            "nombre": u["nombre"],
            "email": u["email"],
            "rol": u["rol"]
        })
    return usuarios
```

---

## ✅ 8. `main.py` – Asegúrate de incluir estas rutas

```python
from app.routes import auth, usuarios

# Añade las rutas de autenticación y gestión de usuarios
app.include_router(auth.router)
app.include_router(usuarios.router)
```

---

# Modo de uso: 

---

## 🧭 1. Acceso a Swagger UI (interfaz web de prueba)

Si corres tu app con:

```bash
uvicorn app.main:app --reload
```

Entonces puedes abrir tu navegador en:

```
http://localhost:8000/docs
```

---

## 🔑 2. Endpoints disponibles y cómo usarlos

### ✅ Registro de usuario

* **Método:** `POST`
* **URL:** `http://localhost:8000/auth/register`
* **Body (JSON):**

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "123456",
  "rol": "cliente"  // Opcional; por defecto es "cliente"
}
```

---

### ✅ Login de usuario

* **Método:** `POST`
* **URL:** `http://localhost:8000/auth/login`
* **Body (JSON):**

```json
{
  "email": "juan@example.com",
  "password": "123456"
}
```

* **Respuesta (JSON):**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
  "token_type": "bearer"
}
```

Guarda ese `access_token`. Lo usarás para autenticarte en las demás rutas.

---

### ✅ Listar usuarios (solo si eres admin)

* **Método:** `GET`
* **URL:** `http://localhost:8000/usuarios/`
* **Headers:**

```http
Authorization: Bearer <tu_access_token>
```

Puedes usarlo así en **curl**:

```bash
curl -H "Authorization: Bearer TU_TOKEN" http://localhost:8000/usuarios/
```

O en **Postman**:

1. Ve a la pestaña "Authorization"
2. Selecciona tipo "Bearer Token"
3. Pega el token ahí

---

## 🧪 Flujo típico de uso

1. **Registrar un usuario (cliente, empleado o admin)**
2. **Hacer login y obtener el token JWT**
3. **Usar ese token para acceder a rutas protegidas según el rol**

   * `admin`: puede listar todos los usuarios
   * `empleado` o `cliente`: no pueden hacerlo

---
