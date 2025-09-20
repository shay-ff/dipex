from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Dipex backend is running!"}