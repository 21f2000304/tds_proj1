from fastapi import FastAPI, HTTPException, Query
from app.task_handler import process_task
from app.file_manager import read_file

app = FastAPI()

@app.post("/run")
async def run_task(task: str = Query(..., description="Describe the task in plain English")):
    try:
        result = process_task(task)
        return {"status": "success", "output": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file_content(path: str):
    content = read_file(path)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"content": content}
