# MediaForge Guard

<p align="center">
  <img src="assets/hero.svg" alt="MediaForge-Guard Architecture" width="100%">
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

<td width="50%" valign="top">

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


<td width="50%" valign="top">

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

Vite proxies `/api` to `VITE_BACKEND_URL`, defaulting to
`http://localhost:8000`. Set `VITE_API_BASE_URL` only when the browser should
call the backend directly instead of using the dev proxy.






















<h2 align="center">📂 Repository Structure</h2>

```text
MediaForge-Guard
│
├── backend
│   ├── api
│   ├── ai_workers
│   ├── models
│   ├── pipelines
│   └── tests
│
├── frontend
│   ├── app
│   ├── components
│   ├── public
│   └── styles
│
├── assets
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
