#!/usr/bin/env python3
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="HeroCal Server", version="1.0.0")

# Prefer serving built frontend from ./dist (e.g., Vite build). Fallback: no homepage.
root_dir = Path(__file__).parent
dist_dir = root_dir / "dist"
if dist_dir.exists():
    # Serve assets (e.g., /assets/*)
    assets_dir = dist_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    def _read_dist_index() -> str:
        return (dist_dir / "index.html").read_text(encoding="utf-8")

    @app.get("/", response_class=HTMLResponse)
    def serve_index():
        return HTMLResponse(content=_read_dist_index())
else:
    @app.get("/", response_class=PlainTextResponse)
    def no_frontend():
        return PlainTextResponse("Frontend not found. Upload/build your Hill-Callories app into ./dist.")

@app.get("/api", response_class=JSONResponse)
def api_root():
    return {"status": "ok", "service": "HeroCal", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/")
async def webhook_root(request: Request):
    # Accept generic webhook payloads at root for ngrok tests
    try:
        payload = await request.json()
    except Exception:
        payload = {"raw": (await request.body()).decode(errors="ignore")}
    return JSONResponse({"received": True, "path": "/", "payload": payload})

@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {"raw": (await request.body()).decode(errors="ignore")}
    return JSONResponse({"received": True, "path": "/webhook", "payload": payload})

@app.get("/env")
def env():
    return {"PORT": os.environ.get("PORT")}


