# Topichub

> Where curious minds gather. Join live rooms, share ideas, and learn out loud.

Topichub is a real-time discussion platform built with Django. Create topic-based
rooms, chat live over WebSockets, follow recent activity, and build a profile —
all wrapped in a clean, modern UI.

> **Note:** This project was previously named *StudyBud / StudyBuddy* and has been
> rebranded to **Topichub**. The internal Django project package is still named
> `studybud` for backwards compatibility (settings module, ASGI/WSGI entrypoints).

---

## Features

- **Topic rooms** — create, edit, and delete rooms grouped by topic.
- **Real-time chat** — messages stream instantly via Django Channels (WebSockets).
- **Live participants** — users are auto-added to a room's participant list.
- **Activity feed** — see the latest replies across all rooms.
- **Topic browsing & search** — filter rooms by topic or free-text search.
- **User profiles** — custom user model with avatar, bio, and hosted rooms.
- **Auth** — email-based registration and login.
- **REST API** — a small DRF surface under `/api/`.
- **Responsive, modern UI** — a fresh design system (`static/styles/topichub.css`).

## Tech Stack

- **Backend:** Django 4.2+, Django REST Framework
- **Realtime:** Django Channels + Daphne (ASGI), in-memory channel layer for dev
- **Database:** SQLite (development default)
- **Frontend:** Django templates + vanilla CSS/JS
- **Images:** Pillow

## Project Structure

```
studybud/
├── base/                 # Main app: models, views, urls, consumers, API
│   ├── api/              # DRF serializers, views, urls
│   ├── templates/base/   # Page templates (home, room, profile, ...)
│   ├── consumers.py      # WebSocket consumer for room chat
│   ├── models.py         # User, Topic, Room, Message
│   └── views.py
├── studybud/             # Project config (settings, asgi, wsgi, urls)
├── templates/            # Base layout + navbar
├── static/               # CSS, JS, images
│   └── styles/topichub.css   # Topichub design system
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## Getting Started

### 1. Clone and enter the project

```bash
git clone https://github.com/VaibhavSiroha/studybud.git
cd studybud
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

> Real-time chat uses ASGI (Daphne/Channels). `runserver` works for local
> development; for production run under an ASGI server, e.g.
> `daphne studybud.asgi:application`.

## Data Model

| Model     | Key fields                                                        |
|-----------|-------------------------------------------------------------------|
| `User`    | `name`, `email` (login field), `bio`, `avatar`                     |
| `Topic`   | `name`                                                             |
| `Room`    | `host`, `topic`, `name`, `description`, `participents`, timestamps |
| `Message` | `user`, `room`, `body`, timestamps                                 |

## API

A minimal REST API is available under `/api/` (see `base/api/urls.py`).

## Configuration Notes

- `DEBUG = True` and a development `SECRET_KEY` are set in
  `studybud/settings.py` — **change these before deploying.**
- Uploaded avatars are stored in `static/images/` (`MEDIA_ROOT`).
- The channel layer is in-memory (dev only). Use `channels-redis` for
  multi-process / production setups.

## License

This project is provided as-is for learning and personal use.
