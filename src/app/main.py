from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.ws import router as ws_router


app = FastAPI(title="WebSocket Relay", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "websocket-relay"}


