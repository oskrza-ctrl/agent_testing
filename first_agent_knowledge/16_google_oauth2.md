---
tags: [google, oauth2, autenticacion, token, credenciales]
---

# Flujo OAuth2 con Google

OAuth2 permite que tu aplicación acceda a datos de Google con permiso explícito del usuario. El primer uso abre un navegador; las siguientes veces usa el token guardado.

## Código completo del flujo

```python
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/tasks"]
CREDENTIALS_FILE = Path("credentials/credentials.json")
TOKEN_FILE = Path("credentials/token.json")

def get_service():
    creds = None

    # 1. Intentar cargar token guardado
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # 2. Si no hay token o está vencido, autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())   # refresh automático
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)  # abre el navegador

        # 3. Guardar token para próxima vez
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("tasks", "v1", credentials=creds)
```

## Primera autenticación

Al correr el código por primera vez:
1. Se abre una ventana del navegador
2. Google pide iniciar sesión
3. Aparece la pantalla de permisos: "Second Brain Agent quiere acceder a tus tareas"
4. El usuario acepta
5. Google redirige a `localhost` (el servidor local temporal de OAuth)
6. El token se guarda en `token.json`

En ejecuciones posteriores: el token se carga desde el archivo y se refresca automáticamente si está vencido.

## Un token por servicio

El proyecto tiene tres tokens independientes para evitar que un scope amplio comprometa los demás servicios:

| Token | Scope | Acceso |
|-------|-------|--------|
| `token.json` | `auth/tasks` | Solo Google Tasks |
| `token_calendar.json` | `auth/calendar.events` | Solo eventos de Calendar |
| `token_drive.json` | `auth/drive` | Google Drive completo |

## Solución de problemas comunes

**"invalid_grant"**: el token está vencido o fue revocado. Borrar `token.json` y autenticar de nuevo.

**"access_denied"**: el email del usuario no está en la lista de usuarios de prueba en Google Cloud Console.

**Scopes insuficientes**: si cambias los scopes, borra el token y vuelve a autenticar.

## Conceptos relacionados

- [[10_autenticacion_apis]] — diferencia con API Keys
- [[15_google_apis_overview]] — setup inicial en Google Cloud Console
- [[17_google_tasks_api]] — uso del servicio de Tasks
