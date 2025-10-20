#!/usr/bin/env python3
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="HeroCal Server", version="1.0.0")

# Serve static site from ./public if present
public_dir = Path(__file__).parent / "public"
if public_dir.exists():
    app.mount("/", StaticFiles(directory=str(public_dir), html=True), name="static")

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


