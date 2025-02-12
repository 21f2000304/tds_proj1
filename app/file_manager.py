import os

def read_file(path: str):
    if not path.startswith("/data/"):
        return None  # Prevent access outside /data

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        return f.read()
