from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Dipex backend is running!"} 

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    # TODO: OCR extraction here
    return {"id": "0", "vendor": "Starbucks", "amount": 350, "currency": "INR", "category": "Food", "date": "2025-01-01"}
