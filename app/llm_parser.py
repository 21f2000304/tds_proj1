import os
import openai

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

def parse_task(task: str):
    prompt = f"""You are an automation assistant. Extract structured task details from the input.

    Task: "{task}"

    Respond in JSON format:
    {{
        "action": "what to do",
        "params": {{
            "key": "value"
        }}
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        api_key=AIPROXY_TOKEN
    )

    return response["choices"][0]["message"]["content"]
