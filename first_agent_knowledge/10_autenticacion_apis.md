---
tags: [api, autenticacion, oauth2, api-key, seguridad]
---

# Autenticación en APIs: API Keys vs OAuth2

Hay dos grandes métodos de autenticación en las APIs que usa este proyecto.

## API Key — acceso directo

Una API Key es un string secreto que identifica a tu aplicación. Es el método más simple.

```python
import openai

client = openai.OpenAI(api_key="sk-proj-...")
# Cada request incluye la key en el header Authorization
```

**Cuándo se usa:** cuando la API pertenece a un servicio externo (OpenAI) y no necesitas acceder a datos de un usuario específico.

**Ventajas:** simple de implementar  
**Riesgos:** si alguien obtiene la key, tiene acceso total hasta que la revoques

## OAuth2 — acceso delegado

OAuth2 permite que tu aplicación acceda a los datos de un usuario de Google (Tasks, Calendar, Drive) **con el permiso explícito del usuario**. El usuario nunca le da su contraseña a tu app.

### Flujo OAuth2 simplificado

```
1. Tu app abre un navegador
      |
      v
2. Google muestra pantalla de permisos:
   "Second Brain Agent quiere acceder a tu Google Tasks"
      |
      v
3. El usuario acepta
      |
      v
4. Google devuelve un código temporal
      |
      v
5. Tu app intercambia el código por un token de acceso
      |
      v
6. Tu app guarda el token en token.json
      |
      v
7. Próximas veces: usa el token guardado (refresh automático)
```

### Cómo se implementa en el proyecto

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/tasks"]

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials/credentials.json",
    SCOPES
)
creds = flow.run_local_server(port=0)  # abre el navegador
```

El archivo `credentials.json` se descarga de Google Cloud Console. El token resultante se guarda en `credentials/token.json`.

### Tokens separados por servicio

El proyecto usa un token diferente para cada API de Google:

| Servicio | Token guardado |
|----------|---------------|
| Google Tasks | `credentials/token.json` |
| Google Calendar | `credentials/token_calendar.json` |
| Google Drive | `credentials/token_drive.json` |

Cada token tiene sus propios scopes (permisos). Si los scopes cambian, el token viejo ya no sirve y hay que autenticar de nuevo.

## Conceptos relacionados

- [[08_python_dotenv]] — guardar API keys en .env
- [[16_google_oauth2]] — flujo OAuth2 completo con código real
- [[15_google_apis_overview]] — configuración de Google Cloud Console
