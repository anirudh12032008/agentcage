from fastAPI import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="battle")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}