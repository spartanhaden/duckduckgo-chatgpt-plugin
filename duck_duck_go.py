#!/usr/bin/env python3
import base64
import json
import pprint
from typing import List

import requests
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, conint

app = FastAPI()

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow any method
    allow_headers=["*"],  # Allow any header
)


@app.post("/search_duckduckgo", summary="Search DuckDuckGo and get the URL of the first result, please just search a single word")
async def search_duckduckgo(query: str) -> JSONResponse:
    """Searches DuckDuckGo and returns the URL of the first search result."""

    search_safe = query.replace(" ", "+")

    url = f'https://api.duckduckgo.com/?q={search_safe}&format=json'

    print(f"url: {url}")

    try:
        response = requests.get(url)
        response_json = response.json()
        print("DuckDuckGo response:")
        pprint.pprint(response_json)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content=response_json, status_code=200)


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest(request: Request):
    host = request.headers['host']
    with open("ai-plugin.json") as f:
        text = f.read().replace("PLUGIN_HOSTNAME", f"https://{host}")
    return JSONResponse(content=json.loads(text))


@app.get("/openapi.json")
async def openapi_spec(request: Request):
    host = request.headers['host']
    with open("openapi.json") as f:
        text = f.read().replace("PLUGIN_HOSTNAME", f"https://{host}")
    return JSONResponse(content=text, media_type="text/json")


if __name__ == "__main__":
    # get public ip
    ip = requests.get('https://api.ipify.org').text

    # print(f"Running on {ip}:6969")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=6969
    )
