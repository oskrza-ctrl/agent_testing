---
tags: [google, apis, cloud-console, credenciales, scopes]
---

# Google APIs — overview y configuración

El proyecto usa tres APIs de Google: Tasks, Calendar y Drive. Todas comparten el mismo mecanismo de autenticación OAuth2 pero tienen scopes y tokens independientes.

## Google Cloud Console

Antes de usar cualquier API de Google, hay que:

1. **Crear un proyecto** en [console.cloud.google.com](https://console.cloud.google.com)
2. **Habilitar la API** deseada (Tasks API, Calendar API, Drive API)
3. **Crear credenciales OAuth 2.0** de tipo "Aplicación de escritorio"
4. **Descargar `credentials.json`** y guardarlo en `credentials/`
5. **Agregar tu email como usuario de prueba** (mientras la app no está verificada)

## credentials.json

Es el archivo de identidad de tu aplicación. No contiene tokens de usuario — solo identifica tu app ante Google. Se descarga una vez desde Google Cloud Console.

```
credentials/
├── credentials.json          ← identidad de la app (no cambiar)
├── token.json                ← token de Google Tasks (generado en 1er uso)
├── token_calendar.json       ← token de Google Calendar
└── token_drive.json          ← token de Google Drive
```

Todo esto está en `.gitignore` — nunca se sube al repositorio.

## Scopes — permisos granulares

Cada API requiere un scope específico. El usuario solo otorga permisos para lo que se declara.

```python
# Google Tasks
SCOPES = ["https://www.googleapis.com/auth/tasks"]

# Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]
```

Si cambias los scopes en el código, el token viejo queda inválido y hay que autenticar de nuevo (borrar el token.json correspondiente).

## Integración opcional

Las tres APIs son opcionales en el proyecto. Si `credentials/credentials.json` no existe, el sistema funciona solo con OpenAI y la Knowledge Base local.

```python
credentials_file = Path("credentials/credentials.json")

tasks_svc = (
    GoogleTasksService(credentials_file)
    if credentials_file.exists() else None
)
```

Esto permite que el sistema funcione en cualquier entorno sin configuración obligatoria.

## Conceptos relacionados

- [[16_google_oauth2]] — flujo completo de autenticación
- [[17_google_tasks_api]] — API de Google Tasks
- [[18_google_calendar_api]] — API de Google Calendar
- [[19_google_drive_api]] — API de Google Drive
- [[10_autenticacion_apis]] — diferencia entre API Key y OAuth2
