# MediaForge Guard

<p align="center">
  <img src="./assests/hero.svg" alt="MediaForge-Guard Architecture" width="100%">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=24&duration=3000&pause=1200&color=FFFFFF&center=true&vCenter=true&width=800&lines=Digital+Content+Cannot+Be+Trusted+by+Appearance+Alone;Synthetic+Media+is+Changing+the+Information+Landscape;MediaForge-Guard+Brings+AI-Powered+Verification;From+Raw+Media+to+Explainable+Evidence" />
</p>

## Overview

The internet has entered an era where digital content can no longer be
trusted by appearance alone.

Generative AI has made synthetic images, manipulated media, and misleading
information increasingly difficult to identify.

MediaForge-Guard addresses this challenge by providing an AI-powered
multimodal verification system that analyzes digital content through
multiple forensic perspectives.

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=24&duration=3000&pause=1200&color=D1D5DB&center=true&vCenter=true&width=800&lines=Why+MediaForge-Guard%3F;Building+Trust+in+the+Age+of+Synthetic+Media;Moving+Beyond+Binary+AI+Predictions" />
</p>

# Why MediaForge-Guard?

With the rapid evolution of generative AI, creating realistic synthetic
content has become easier than ever.

Images, text, and digital media can now be manipulated at a scale where
traditional verification methods are no longer sufficient.

Most detection systems answer only:

> "Is this content fake or real?"

MediaForge-Guard focuses on a deeper question:

> "What evidence suggests that this content may not be authentic?"


## Our Vision

MediaForge-Guard aims to build a transparent and explainable verification
system where AI does not only classify content but also provides insights
behind its decisions.

| Challenge | MediaForge-Guard Approach |
|------------|---------------------------|
| Synthetic media generation | AI-powered forensic analysis |
| Black-box predictions | Explainable evidence generation |
| Single-model detection | Multi-agent verification pipeline |
| Growing misinformation | Automated authenticity assessment |


<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=24&duration=3000&pause=1200&color=D1D5DB&center=true&vCenter=true&width=800&lines=Core+Capabilities;Engineering+Trust+Into+Digital+Media;Built+With+Modular+AI+Forensic+Systems" />
</p>


<h1 align="center">Key Features</h1>


<p align="center">
MediaForge-Guard combines artificial intelligence, forensic analysis,
and explainable reporting into a unified media verification workflow.
</p>


<table>
<tr>

<td width="50%">

<h3>🔍 Multimodal Media Analysis</h3>

Analyze digital content through multiple AI-driven perspectives.

<br>

<b>Capabilities:</b>

<ul>
<li>Image analysis</li>
<li>Text analysis</li>
<li>Metadata inspection</li>
<li>Forensic feature extraction</li>
</ul>

Each module contributes independent evidence toward the final verification result.

</td>


<td width="50%">

<h3>🧠 AI Detection Pipeline</h3>

A modular AI pipeline where specialized components collaborate instead of relying on a single prediction model.

<br>

<b>Enables:</b>

<ul>
<li>Independent model evaluation</li>
<li>Flexible model replacement</li>
<li>Scalable inference workflows</li>
<li>Future media expansion</li>
</ul>

</td>

</tr>


<tr>

<td width="50%">

<h3>📄 Explainable Verification Reports</h3>

Transform raw AI predictions into structured forensic insights.

<br>

<b>Reports include:</b>

<ul>
<li>Detection results</li>
<li>Confidence information</li>
<li>Evidence summaries</li>
<li>Analysis explanations</li>
</ul>

</td>


<td width="50%">

<h3>⚙️ Modular Architecture</h3>

Designed for continuous improvement and scalability.

<br>

<b>Supports:</b>

<ul>
<li>Adding new AI agents</li>
<li>Replacing models</li>
<li>Independent component scaling</li>
<li>Future integrations</li>
</ul>

</td>

</tr>


<tr>

<td width="50%">

<h3>📊 Evidence-Based Analysis</h3>

Move beyond simple classification.

<br>

Instead of only answering:

<blockquote>
"Is this fake?"
</blockquote>

MediaForge-Guard investigates:

<blockquote>
"What signals indicate manipulation?"
</blockquote>

</td>


<td width="50%">

<h3>🔐 Secure Processing Workflow</h3>

A controlled backend workflow managing:

<ul>
<li>Media uploads</li>
<li>AI inference</li>
<li>Processing states</li>
<li>Report generation</li>
<li>Data handling</li>
</ul>

</td>

</tr>

</table>

---

## Deployment Architecture

### Current Production Setup (Vercel + Railway)

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend (Vercel)                                           │
│ https://mediaforge-guard.vercel.app                         │
│ • Next.js / Vite SPA                                        │
│ • Static hosting + CDN                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ├─────────────────────────────────────────┐
                   │                                         │
        ┌──────────▼─────────────┐            ┌──────────────▼──────┐
        │ Railway API Services   │            │ Railway Databases   │
        │                        │            │                     │
        │ • api-slim (8080)      │────────────┤ • PostgreSQL        │
        │   FastAPI + Uvicorn   │    TCP     │ • Redis (Broker)    │
        │                        │            │                     │
        │ • worker               │────────────┤ • Supabase Storage  │
        │   Celery Worker        │            │   (S3-compatible)   │
        │   async processing    │            │                     │
        └────────────────────────┘            └─────────────────────┘
```

### Services Configuration

**api-slim** (FastAPI Backend)
- Deployment: `https://api-slim-production.up.railway.app`
- Port: 8080
- Healthcheck: `/health`
- Docstring: `/docs` (Swagger UI)
- Handles: file uploads, user auth, report generation

**worker** (Celery Task Worker)
- Runs on Railway
- Processes analysis tasks asynchronously
- Connects to Redis broker and PostgreSQL

**Postgres** (Railway)
- Analysis results and metadata
- User sessions and API keys
- Volume: 500 MB persistent storage

**Redis** (Railway)
- Celery task broker
- Result backend caching
- Volume: 500 MB persistent storage

**Supabase Storage**
- Media uploads and processed files
- S3-compatible bucket access

---

## Deployment Instructions

### Local Development

#### Backend Setup

Create a virtual environment:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
```

Copy and configure environment file:

```bash
cp backend/.env.example backend/.env
```

In `backend/.env`:
- Set `JWT_SECRET_KEY` to a unique 32-character string
- Set `ENVIRONMENT=development`
- Point `DATABASE_URL` to local or Railway Postgres
- Point `REDIS_URL` to local or Railway Redis

Run the API:

```bash
cd backend
../backend/.venv/bin/uvicorn app.main:app --reload --port 8000
```

Access API: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

#### Frontend Setup

Install and run Vite:

```bash
cd frontend
npm install
npm run dev
```

Access frontend: `http://localhost:5173`  
Vite proxies `/api` to `VITE_API_BASE_URL` (defaults to `http://localhost:8000`)

#### Run Backend Tests

```bash
cd backend
../backend/.venv/bin/pytest
```

---

## Docker Deployment

The production Docker setup includes:

- **frontend**: Static Vite build served by Nginx (port 5173)
- **api-slim**: FastAPI backend (port 8000)
- **worker**: Celery worker (async task processing)
- **postgres**: PostgreSQL database
- **redis**: Redis for Celery broker

### Local Docker Compose

Copy the Docker environment file:

```bash
cp backend/docker.env.example backend/.env.docker
```

Update `backend/.env.docker` with production secrets:
- Unique `JWT_SECRET_KEY`
- Strong PostgreSQL password
- Supabase credentials

Start the stack:

```bash
docker compose up --build
```

App will be available at: `http://localhost:5173`

---

## Environment Variables

### Backend Configuration

```env
# Core settings
ENVIRONMENT=production  # development or production
JWT_SECRET_KEY=<unique_32_char_secret>

# Database & Cache
DATABASE_URL=postgresql://user:pass@postgres.railway.internal:5432/mediaforge
REDIS_URL=redis://default:pass@redis.railway.internal:6379/0

# Celery
CELERY_BROKER_URL=<same_as_REDIS_URL>
CELERY_RESULT_BACKEND=<same_as_REDIS_URL>

# LLM Provider (for analysis)
LLM_PROVIDER=groq
GROQ_API_KEY=<your_groq_api_key>
GROQ_MODEL=mixtral-8x7b-32768

# Frontend CORS
CORS_ORIGINS=https://mediaforge-guard.vercel.app,http://localhost:5173

# Media constraints
MAX_UPLOAD_SIZE_BYTES=104857600  # 100MB
DISABLED_MEDIA_TYPES=video/mp4,audio/mpeg  # Disabled in hosted demo

# Supabase Storage
SUPABASE_URL=<your_supabase_project_url>
SUPABASE_STORAGE_BUCKET=mediaforge-uploads
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>
```

### Restrictions in Hosted Demo

- **Video uploads**: Disabled (CPU-heavy, requires Modal/RunPod)
- **Audio uploads**: Disabled (requires dedicated processing)
- **Max file size**: 100 MB
- **Supported formats**: JPEG, PNG, GIF (images only)

Future heavy processing can be offloaded to **Modal** or **RunPod** for scaling.

---

## Repository Structure

```text
MediaForge-Guard/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── core/            # Config, security, Celery
│   │   └── analysis/        # AI verification pipeline
│   ├── Dockerfile           # Slim API image
│   ├── Worker.Dockerfile    # Celery worker image
│   ├── Combined.Dockerfile  # Legacy combined image (deprecated)
│   ├── requirements.txt      # Python dependencies
│   └── tests/               # Pytest suite
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable UI components
│   │   └── api/             # API client hooks
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite bundler config
│
├── docker-compose.yml       # Local multi-container setup
├── .env.example             # Environment template
└── README.md                # This file
```

---

## Troubleshooting

### API won't start

**Symptom:** Deployment fails with "JWT_SECRET_KEY is still the placeholder"

**Fix:** Update `JWT_SECRET_KEY` to a unique 32-character string and redeploy.

### Worker tasks not processing

**Symptom:** Analysis jobs queue but never execute

**Action needed:** 
1. Check worker is online: `https://railway.com/project/[id]`
2. Verify Redis URL matches between `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`
3. Check worker logs for connection errors

### Upload fails with 413 Payload Too Large

**Symptom:** Files over 100 MB are rejected

**Fix:** Increase `MAX_UPLOAD_SIZE_BYTES` in environment (requires API redeploy)

### Frontend can't reach API

**Symptom:** CORS errors or 404 on `/api` routes

**Fix:** 
- In development: Vite proxy handles this automatically
- In production: Frontend must call same-origin `/api`, or update `CORS_ORIGINS` env var

---

## Future Enhancements

### Phase 1: Database & Cache Migration (Optional)
- **Upstash Redis**: Replace Railway Redis (better free tier)
- **Supabase Postgres**: Replace Railway Postgres (unified data stack)

### Phase 2: Heavy Processing Offload
- **Modal.com** or **RunPod**: Video/audio analysis
- **LangChain** or **LlamaIndex**: Advanced LLM pipelines
- Async job queue for batch analysis

### Phase 3: Advanced Features
- Multi-format media support (restore video/audio)
- Real-time forensic visualization
- Collaborative report generation
- Custom domain & branding

---

<p align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</p>

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&size=18&duration=4000&pause=1500&color=C7A86A&center=true&vCenter=true&width=700&lines=Building+Trust+in+Digital+Media.;Multi-Agent+AI+for+Content+Verification.;MediaForge-Guard." />

</p>

<p align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</p>

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=18&duration=3500&pause=1500&color=C7A86A&center=true&vCenter=true&width=750&lines=Built+with+%E2%9D%A4%EF%B8%8F+for+trustworthy+digital+media.;Created+by+Rashmi+Jha+%26+Richa+Gupta." />

</p>

