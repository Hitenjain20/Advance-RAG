import os
from dotenv import load_dotenv
from llm import Inference
from fastapi import FastAPI, HTTPException, File, UploadFile

load_dotenv()

inference = Inference()

app = FastAPI()

# Variable to store the uploaded file path
uploaded_file_path = None

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location

    if not os.path.exists("temp"):
        os.makedirs("temp")

    uploaded_file_path = f"temp/{file.filename}"
    with open(uploaded_file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "PDF uploaded successfully", "file_path": uploaded_file_path}

@app.post("/query_pdf")
async def query_pdf(query: str, file_path: str = None):
    # Check if file_path is provided
    if not file_path:
        raise HTTPException(status_code=400, detail="Missing file path")

    # Use the provided file path for processing
    response = inference._query_engine(file_path, query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("App:app", reload=True)
