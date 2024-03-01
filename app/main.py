from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

app = FastAPI(
    docs_url="/documentation",
    redoc_url="/redocumentation",
    root_path="/peoplecheb",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian",
        "filter": "true",
        "tryItOutEnabled": "true",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, workers=10, reload=True)
