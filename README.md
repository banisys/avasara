# Persian Speech To Text API

FastAPI based speech-to-text service using Faster-Whisper and MySQL.

This project uploads Persian audio files (`mp3`, `wav`), stores them on disk, generates a unique file token, and converts speech to text asynchronously using Faster-Whisper (`large-v3` model on CPU).

---

# Features

- FastAPI
- Docker & Docker Compose
- MySQL
- phpMyAdmin
- Alembic Migration
- Faster-Whisper
- Background transcription processing
- Persian speech recognition
- File token system
- Status tracking

---

# Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- MySQL 8
- Docker
- Faster-Whisper
- FFmpeg

---

# Project Structure

```txt
project/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── file.py
│   ├── routers/
│   │   └── gateway.py
│   ├── services/
│   │   ├── file_service.py
│   │   └── transcribe_service.py
│   └── uploads/
│
├── alembic/
├── uploads/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

# Requirements

- Docker
- Docker Compose

---

# Run Project

## Build & Start

```bash
docker compose up --build
```

---

# Services

| Service | URL |
|---|---|
| FastAPI | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| phpMyAdmin | http://localhost:8080 |

---

# phpMyAdmin Login

| Key | Value |
|---|---|
| Server | mysql |
| Username | root |
| Password | 123456 |

---

# Database Migration

## Create Migration

```bash
docker compose exec api alembic revision --autogenerate -m "migration name"
```

## Run Migration

```bash
docker compose exec api alembic upgrade head
```

---

# API Endpoint

## Route

```txt
POST /api/ocr/getway
```

---

# Commands

| Command | Description |
|---|---|
| addfile | Upload audio file |
| convert | Start speech-to-text conversion |
| checkconvert | Check conversion result |

---

# 1. Upload File

## Request

```bash
curl -X POST "http://localhost:8000/api/ocr/getway" \
  -F "command=addfile" \
  -F "filehandle=@./test.mp3"
```

## Response

```json
{
  "Status": "Done",
  "FileToken": "Nzrwxxxxxxxx4f3e5"
}
```

---

# 2. Start Convert

## Request

```bash
curl -X POST "http://localhost:8000/api/ocr/getway" \
  -F "command=convert" \
  -F "filetoken=Nzrwxxxxxxxx4f3e5"
```

## Response

```json
{
  "Status": "ConvertStarted"
}
```

---

# 3. Check Convert Result

## Request

```bash
curl -X POST "http://localhost:8000/api/ocr/getway" \
  -F "command=checkconvert" \
  -F "filetoken=Nzrwxxxxxxxx4f3e5"
```

## Response

```json
{
  "Status": "finished",
  "Output": "متن خروجی فایل صوتی"
}
```

---

# File Status Values

```txt
pending
processing
finished
failed
cancelled
```

---

# Supported Formats

- mp3
- wav

---

# Whisper Model Configuration

| Option | Value |
|---|---|
| Model | large-v3 |
| Device | CPU |
| Compute Type | float32 |
| Language | Persian (`fa`) |

---

# Notes

- First model download may take several minutes.
- `large-v3` on CPU is heavy and requires significant RAM.
- FFmpeg is required and installed inside Docker container.

---

# Useful Commands

## Stop Containers

```bash
docker compose down
```

## Rebuild Containers

```bash
docker compose up --build
```

## Enter API Container

```bash
docker compose exec api sh
```

## Enter MySQL Container

```bash
docker compose exec mysql bash
```

---

# License

MIT