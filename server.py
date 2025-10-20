#!/usr/bin/env python3
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="HeroCal Server", version="1.0.0")

@app.get("/")
def root():
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


