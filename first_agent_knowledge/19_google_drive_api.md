---
tags: [google, drive, api, archivos, integracion]
---

# Google Drive API

Google Drive API permite listar, descargar, subir y mover archivos desde código. El proyecto la usa para conectar el pipeline con la nube: los audios llegan desde Drive, y la Knowledge Base se sincroniza de vuelta a Drive.

## Flujo del proyecto con Drive

```
Drive/second_brain/inbox/audio.mp3
        |
        v  (DriveAgent.download_inbox)
local/input/audio.mp3
        |
        v  (pipeline completo)
local/Knowledge_Base/**
        |
        v  (DriveAgent.upload_kb_file)
Drive/second_brain/knowledge_base/**
        |
        v  (DriveAgent.move_to_processed)
Drive/second_brain/processed/audio.mp3
```

## Operaciones principales

```python
# Listar MP3 en una carpeta de Drive
results = service.files().list(
    q=f"'{folder_id}' in parents and mimeType='audio/mpeg' and trashed=false",
    fields="files(id, name)"
).execute()
files = results.get("files", [])

# Descargar un archivo
request = service.files().get_media(fileId=file_id)
with open(local_path, "wb") as f:
    downloader = MediaIoBaseDownload(f, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

# Subir un archivo (crearlo en Drive)
media = MediaFileUpload(str(local_path), resumable=True)
service.files().create(
    body={"name": filename, "parents": [folder_id]},
    media_body=media
).execute()

# Mover un archivo a otra carpeta
service.files().update(
    fileId=file_id,
    addParents=processed_folder_id,
    removeParents=inbox_folder_id
).execute()
```

## Actualizar sin duplicar

Los archivos acumulativos (`ideas.md`, `tasks.md`) se actualizan con cada ejecución. Si se subiera como nuevo cada vez, habría cientos de copias en Drive.

La solución: antes de subir, verificar si el archivo ya existe y actualizarlo:

```python
def upload_file(self, local_path: Path, folder_id: str) -> str:
    existing_id = self._find_existing(local_path.name, folder_id)
    if existing_id:
        # Actualizar contenido del archivo existente
        media = MediaFileUpload(str(local_path), resumable=True)
        self.service.files().update(
            fileId=existing_id,
            media_body=media
        ).execute()
    else:
        # Crear nuevo archivo
        ...
```

## Configuración — folder IDs

Los IDs de carpeta se configuran en `.env`:

```
GOOGLE_DRIVE_INBOX_FOLDER_ID=1pgehcCoulbemk_c1XmF1WOMQ-iwYEWPz
GOOGLE_DRIVE_PROCESSED_FOLDER_ID=1a0xbNnV4R19Fv6LZjrWZnQOHW7BUh_c0
GOOGLE_DRIVE_KB_FOLDER_ID=1rtYFbFItvoZrI1V0xN018mLU-3uOoy9r
```

El ID de una carpeta está en la URL de Drive: `drive.google.com/drive/folders/{ID}`.

## Integración opcional

Si los IDs no están configurados, el sistema usa carpetas locales y no intenta conectarse a Drive.

## Conceptos relacionados

- [[16_google_oauth2]] — autenticación con token_drive.json
- [[15_google_apis_overview]] — scopes y credenciales
- [[25_knowledge_base]] — qué archivos se sincronizan a Drive
