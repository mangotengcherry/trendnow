# TrendPulse

A real-time Google Trends visualizer that displays trending searches with related news articles and social media reactions.

## Tech Stack

- **Frontend**: Vue 3, Vite, TypeScript, Pinia, Vue Router, Axios
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Auth**: Google OAuth 2.0 + JWT password-based login

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`. The Vite dev server proxies `/api` requests to the backend.

### Environment Variables

| Variable | Location | Description |
|---|---|---|
| `SECRET_KEY` | Backend | JWT signing key |
| `GOOGLE_CLIENT_ID` | Backend | Google OAuth client ID |
| `VITE_API_URL` | Frontend `.env` | API base URL (defaults to `/api`) |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/google` | Google OAuth token verification |
| `POST` | `/api/auth/login` | Password-based login |
| `POST` | `/api/auth/password` | Set/change password (authenticated) |
| `GET` | `/api/trends?country=` | Get trending keywords by country |
| `GET` | `/api/related/{keyword}` | Get news and social posts for a keyword |

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── routers/             # API route handlers (auth, trends)
│   ├── services/            # Business logic (trend fetching)
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth_utils.py        # JWT and password utilities
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/           # Page components (Home, Login, Profile)
│   │   ├── components/      # UI components (TrendList, TrendDetail)
│   │   ├── stores/          # Pinia state management
│   │   ├── services/        # API client
│   │   └── router/          # Vue Router config
│   └── vite.config.js
├── agent.md                 # 3-layer architecture instructions
└── CLAUDE.md                # AI assistant guidance
```

## Deployment

Configured for Heroku via `backend/Procfile`:

```bash
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
