# MediaForge Vision Modal Service

This service moves the heavy MediaForge Vision PyTorch inference off Railway.
Railway still handles uploads, preprocessing, Celery orchestration, database
writes, reports, and frontend polling.

## 1. Install Modal locally

```bash
python3 -m pip install modal
modal setup
```

## 2. Create the Modal secret

Use the same Hugging Face read token that can access the private model repo.
Choose a random `MODAL_API_TOKEN`; Railway will use it as the bearer token.

```bash
modal secret create mediaforge-vision-secrets \
  HF_TOKEN=hf_xxx \
  MEDIAFORGE_VISION_REPO_ID=rashmijha06/mediaforge_vision \
  MEDIAFORGE_VISION_FILENAME=mediaforge_vision_v1.pth \
  MODAL_API_TOKEN=replace-with-random-token
```

## 3. Test temporarily

```bash
modal serve modal/modal_vision_service.py
```

Modal prints a temporary public URL. The prediction endpoint is:

```text
https://...modal.run/predict
```

## 4. Deploy permanently

```bash
modal deploy modal/modal_vision_service.py
```

Copy the deployed `/predict` URL into Railway:

```text
VISION_INFERENCE_PROVIDER=modal
MODAL_VISION_ENDPOINT_URL=https://...modal.run/predict
MODAL_API_TOKEN=replace-with-random-token
```

## 5. Expected Runtime Flow

```text
Railway worker
  -> preprocesses image
  -> POSTs processed image to Modal /predict
  -> Modal runs MediaForge Vision on GPU
  -> Railway stores the returned label/confidence/probabilities
```
