# MediaForge Guard

## Backend

Create a virtual environment and install dependencies:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r requirements.txt
```

Copy `backend/.env.example` to `backend/.env` and set a unique
`JWT_SECRET_KEY`. Keep `ENVIRONMENT=development` locally. In production,
the app refuses to start if `JWT_SECRET_KEY` is still the placeholder.

Run the API from the backend directory:

```bash
cd backend
../backend/.venv/bin/uvicorn app.main:app --reload
```

Run backend tests:

```bash
backend/.venv/bin/pytest
```

## Frontend

Install dependencies and run Vite:

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `VITE_BACKEND_URL`, defaulting to
`http://localhost:8000`. Set `VITE_API_BASE_URL` only when the browser should
call the backend directly instead of using the dev proxy.
