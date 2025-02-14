# /// script
# requires-python = ">=3.13"
# dependencies = [
# "fastapi",
# "uvicorn",
# "requests",
# ]
# ///

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# Define the working directory for storing scripts
DATA_DIR = "/data"

# Corrected tools JSON structure
tools = [
    {
        "type": "function",
        "function": {
            "name": "script_runner",
            "description": "Install a package and run a script from a URL with provided arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_url": {
                        "type": "string",
                        "description": "URL to the script."
                    },
                    "args": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of arguments to pass to the script."
                    }
                },
                "required": ["script_url", "args"]
            }
        }
    }
]

# Fix: Ensure AIPROXY_TOKEN is correctly set
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN", "").strip()
if not AIPROXY_TOKEN:
    raise ValueError("Missing AIPROXY_TOKEN! Set it as an environment variable.")

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI app!"}

@app.post("/run")
def task_runner(task: str):
    print(f"Received task: {task}")  # Log the task input

    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": task}
        ],
        "tools": tools,
        "tool_choice": "auto"
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"OpenAI API response: {response.json()}")  # Log the response

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error calling OpenAI API")

    try:
        result = response.json()
        tool_calls = result["choices"][0]["message"].get("tool_calls", [])
        if not tool_calls:
            raise HTTPException(status_code=500, detail="No tool calls returned")

        arguments_str = tool_calls[0]["function"]["arguments"]
        arguments = json.loads(arguments_str)

        script_url = arguments["script_url"]
        args = arguments["args"]
        if not args or not isinstance(args, list):
            raise HTTPException(status_code=400, detail="Invalid script arguments")

        email = args[0]  # First argument is email

        # Download the script
        script_path = os.path.join(DATA_DIR, os.path.basename(script_url))
        print(f"Saving script to: {script_path}")  # Log the file path
        script_content = requests.get(script_url)
        print(f"Script download status: {script_content.status_code}")  # Log the status code
        if script_content.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download script")

        # Save the script to the /data directory
        try:
            with open(script_path, "wb") as f:
                f.write(script_content.content)
            print(f"Script saved successfully to: {script_path}")  # Log success
        except Exception as e:
            print(f"Error saving script: {str(e)}")  # Log any errors
            raise HTTPException(status_code=500, detail=f"Error saving script: {str(e)}")

        # Verify the script file exists
        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail="Script file not found after download")

        # Execute the script with arguments using `uv`
        command = ["uv", "run", script_path, email]
        print(f"Executing command: {command}")  # Log the command
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")  # Log the output
        print(f"Command error: {result.stderr}")  # Log the error

        return {"output": result.stdout, "error": result.stderr}

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)