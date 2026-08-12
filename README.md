# MediaForge Guard

> AI-assisted media verification for images, video, audio, text, and public media URLs.

**Live Project:** [MediaForge-Gaurd Live Demo](https://media-forge-gaurd-v1.vercel.app/)

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

MediaForge-Guard addresses this challenge with an AI-powered multimodal
verification system for images, video, audio, text, and supported public
media URLs. The system combines lightweight orchestration on Railway with
GPU-backed inference on Modal for heavier model workloads.

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=24&duration=3000&pause=1200&color=D1D5DB&center=true&vCenter=true&width=800&lines=Why+MediaForge-Guard%3F;Building+Trust+in+the+Age+of+Synthetic+Media;Moving+Beyond+Binary+AI+Predictions" />
</p>

# Demo Video
<p align="center">
  <a href="https://youtu.be/Y1RfYltdC1U">
    <img src="./assests/MediaForgeGaurd_thumbnail.png" width="600" alt="MediaForge Guard Demo">
  </a>
</p>
<p align="center">
  <strong>🎥 Click the image above to watch the full demo.</strong>
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

<td width="50%" valign="top">

<h3>🔍 Multimodal Media Analysis</h3>

Analyze digital content through multiple AI-driven perspectives.

<br>

<b>Capabilities:</b>

<ul>
<li>Image analysis</li>
<li>Video frame analysis</li>
<li>Audio transcription and audio signals</li>
<li>Text analysis</li>
<li>Direct URL, YouTube, and Reddit media ingestion</li>
<li>Metadata inspection</li>
<li>Forensic feature extraction</li>
</ul>

Each module contributes independent evidence toward the final verification result.

</td>


<td width="50%" valign="top">

<h3>🧠 AI Detection Pipeline</h3>

A modular AI pipeline where specialized components collaborate instead of relying on a single prediction model.

<br>

<b>Enables:</b>

<ul>
<li>Independent model evaluation</li>
<li>Flexible model replacement</li>
<li>Modal GPU inference for heavy image/video/audio work</li>
<li>Queue isolation for image, text, video, and audio jobs</li>
</ul>

</td>

</tr>


<tr>

<td width="50%" valign="top">

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


<td width="50%" valign="top">

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

<td width="50%" valign="top">

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


<td width="50%" valign="top">

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





<p align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</p>


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

Vite proxies `/api` to `VITE_API_BASE_URL`, defaulting to
`http://localhost:8000`. Use a relative value or leave it empty when the
browser should call same-origin `/api` routes in production.

Frontend media visibility is controlled at build time with:

```bash
VITE_DISABLED_EXTENSIONS=
```

Set it to an empty value to show all supported uploads. During earlier staged
deployments, this was used to hide heavy media:

```bash
VITE_DISABLED_EXTENSIONS=mp4,mp3,wav
VITE_DISABLED_EXTENSIONS=mp3,wav
```

Because Vite bakes env vars into the frontend bundle, changing this value
requires rebuilding/redeploying the frontend.

## Current V2 Architecture

```text
Frontend
  -> FastAPI API
  -> Supabase Storage
  -> Celery + Upstash Redis
  -> Railway worker orchestration
       -> lightweight preprocessing
       -> Modal GPU endpoints for heavy inference
       -> database persistence
       -> report generation
  -> frontend progress/results views
```

Media-specific flow:

```text
Image
  -> Railway preprocessing
  -> Modal Vision /predict
  -> forensic evidence + report

Video
  -> Railway extracts capped sampled frames
  -> each frame uses lightweight Modal-backed vision prediction
  -> Railway aggregates highest-risk frame
  -> report

Audio
  -> Railway prepares audio
  -> Modal Audio /transcribe
  -> local lightweight audio evidence aggregation
  -> report

Text
  -> Railway text/fact-check/fusion agents
  -> report
```

Public URL ingestion currently supports:

- direct media URLs
- YouTube via `yt-dlp`
- Reddit image/video media posts

Instagram, X, TikTok, and Facebook links are detected but intentionally return
clear unsupported-platform messages.

## Modal GPU Services

Heavy inference is separated from Railway:

- `modal/modal_vision_service.py`
  - endpoint: `/predict`
  - used for image uploads and sampled video frames
  - loads `rashmijha06/mediaforge_vision/mediaforge_vision_v1.pth`
- `modal/modal_audio_service.py`
  - endpoint: `/transcribe`
  - used for Whisper transcription

Deploy:

```bash
modal deploy modal/modal_vision_service.py
modal deploy modal/modal_audio_service.py
```

Railway API and worker env vars:

```bash
VISION_INFERENCE_PROVIDER=modal
MODAL_VISION_ENDPOINT_URL=https://...modal.run/predict

AUDIO_INFERENCE_PROVIDER=modal
MODAL_AUDIO_ENDPOINT_URL=https://...modal.run/transcribe

MODAL_API_TOKEN=<shared-random-token>
DISABLED_MEDIA_TYPES=[]
```

Do not use Modal dashboard URLs such as `https://modal.com/apps/...` for
Railway endpoint configuration. Use deployed `*.modal.run` URLs.

## Production Safeguards

- Separate Celery queues for image, text, video, and audio.
- Heavy-media capacity guard to avoid overloading free-tier workers.
- Stale processing recovery for worker SIGKILL/redeploy cases.
- Video frame caps and 1 FPS sampling to limit compute and latency.
- Safe MIME fallback for direct uploads detected as `application/octet-stream`
  when the file extension is a known supported media type.

## Docker Deployment

The production-style Docker setup uses:

- `frontend`: static Vite build served by Nginx
- `api`: FastAPI backend
- `worker`: Celery worker using the same backend image
- `db`: PostgreSQL
- `redis`: Celery broker and result backend
- Modal: external GPU inference for vision and audio

Create the Docker environment file:

```bash
cp backend/docker.env.example backend/.env.docker
```

Before production deployment, replace `JWT_SECRET_KEY` and the Postgres
password values. Postgres is recommended for deployment; SQLite should only
be used for local development or quick demos.

Start the stack:

```bash
docker compose up --build
```

Open the app at `http://localhost:5173`. The frontend proxies `/api` to the
backend container, so the production build can use same-origin API requests.






















<h2 align="center">📂 Repository Structure</h2>

```text
MediaForge-Guard
│
├── backend
│   ├── app
│   ├── scripts
│   ├── storage
│   └── tests
│
├── ai_workers
│   └── src
│       ├── agents
│       ├── audio_forensics
│       ├── clients
│       ├── pipelines
│       └── processors
│
├── frontend
│   ├── src
│   ├── components
│   └── styles
│
├── modal
│   ├── modal_vision_service.py
│   └── modal_audio_service.py
│
├── ml
│   ├── datasets
│   ├── models
│   └── training
│
├── assests
│   ├── hero.svg
│   └── screenshots
│
└── README.md
```

---


<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&size=18&duration=4000&pause=1500&color=C7A86A&center=true&vCenter=true&width=700&lines=Building+Trust+in+Digital+Media.;Multi-Agent+AI+for+Content+Verification.;MediaForge-Guard."/>

</p>

<p align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</p>


<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=18&duration=3500&pause=1500&color=C7A86A&center=true&vCenter=true&width=750&lines=Built+with+%E2%9D%A4%EF%B8%8F+for+trustworthy+digital+media.;Created+by+Rashmi+Jha+%26+Richa+Gupta." />

</p>
