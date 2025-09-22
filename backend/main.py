from fastapi import FastAPI, UploadFile, File
from .app.api.v1.ocr import router as ocr_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Dipex backend is running!"}

app.include_router(ocr_router, prefix="/api/v1")