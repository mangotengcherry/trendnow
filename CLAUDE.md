# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TrendPulse - A Google Trends Visualizer that displays real-time trending searches with related news and social media reactions. Full-stack app with Vue 3 frontend and FastAPI backend.

## 3-Layer Architecture

This project follows a 3-layer architecture (see `agent.md` for full details):

1. **Directives** (`directives/`) - SOPs in Markdown defining goals, inputs, tools, outputs
2. **Orchestration** - AI agent layer for intelligent routing and decision-making
3. **Execution** (`execution/`) - Deterministic Python scripts for API calls, data processing, etc.

Key principle: push complexity into deterministic code rather than doing everything inline. Check `execution/` for existing scripts before writing new ones. When errors occur, fix the script, test it, and update the relevant directive.

## Development Commands

### Backend (FastAPI + Python)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vue 3 + Vite + TypeScript)

```bash
cd frontend
npm install
npm run dev       # Dev server at http://localhost:5173
npm run build     # Production build to dist/
npm run preview   # Preview production build
```

Both servers must run simultaneously for development. The Vite dev server proxies `/api` requests to `http://localhost:8000`.

### Deployment

Heroku via Procfile: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Tech Stack

- **Frontend**: Vue 3, Vite, Pinia (state), Vue Router, Axios, TypeScript, vue3-google-login
- **Backend**: FastAPI, SQLAlchemy (SQLite), JWT auth (python-jose), bcrypt (passlib), trendspy, feedparser
- **Database**: SQLite at `backend/sql_app.db`

## Architecture Notes

### Backend
- `main.py` - App initialization, CORS config, router mounting
- `routers/auth.py` - Google OAuth token verification + password-based login, returns JWT
- `routers/trends.py` - Trending keywords and related news/social endpoints
- `services/trend_service.py` - Core business logic: trendspy integration, Google News RSS parsing, simulated social posts. Falls back to mock data on API failure.
- `auth_utils.py` - JWT creation/verification, password hashing
- `models.py` / `schemas.py` - SQLAlchemy User model and Pydantic schemas

### Frontend
- `src/stores/auth.ts` - Pinia store managing user state, tokens (persisted to localStorage), and Authorization headers
- `src/router/index.ts` - Routes with auth guard on `/profile`
- `src/views/HomeView.vue` - Main view composing TrendList (sidebar with country selector) + TrendDetail (news + social posts)
- `src/services/api.ts` - Axios client with base URL `/api`

### Auth Flow
Google OAuth or password login -> backend verifies -> returns JWT (24h expiry) -> frontend stores in localStorage and sets on Axios headers. Mock tokens (`mock_token_` prefix) are accepted in dev mode.

### API Endpoints
- `POST /api/auth/google` - Google OAuth token verification
- `POST /api/auth/login` - Password login
- `POST /api/auth/password` - Set/change password (authenticated)
- `GET /api/trends?country=united_states|south_korea` - Trending keywords
- `GET /api/related/{keyword}` - News articles and social posts for a keyword

## File Organization

- `.tmp/` - Intermediate/temp files (never commit, always regenerated)
- `execution/` - Deterministic Python scripts
- `directives/` - SOP markdown files
- Deliverables go to cloud services (Google Sheets/Slides), not local files
