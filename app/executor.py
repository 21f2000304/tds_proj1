import subprocess
import json
import sqlite3
from datetime import datetime

def install_uv_and_run_datagen(user_email: str):
    subprocess.run(["pip", "install", "--user", "uv"], check=True)
    subprocess.run(["python", "datagen.py", user_email], check=True)
    return "Data generation complete."

def count_wednesdays(input_file: str, output_file: str):
    with open(input_file, "r") as f:
        dates = [line.strip() for line in f]

    count = sum(1 for date in dates if datetime.strptime(date, "%Y-%m-%d").weekday() == 2)

    with open(output_file, "w") as f:
        f.write(str(count))

    return f"Wednesdays counted: {count}"
