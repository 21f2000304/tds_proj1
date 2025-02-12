from app.llm_parser import parse_task
from app.executor import *

TASK_MAPPING = {
    "install_uv_and_run_datagen": install_uv_and_run_datagen,
    "format_file": format_file,
    "count_wednesdays": count_wednesdays,
    "sort_contacts": sort_contacts,
    "extract_first_lines": extract_first_lines,
    "index_markdown_files": index_markdown_files,
    "extract_email": extract_email,
    "extract_credit_card": extract_credit_card,
    "find_similar_comments": find_similar_comments,
    "calculate_sales": calculate_sales,
    "fetch_api_data": fetch_api_data,
    "git_operations": git_operations,
    "run_sql_query": run_sql_query
}

def process_task(task: str):
    parsed_task = parse_task(task)
    action = parsed_task["action"]
    params = parsed_task["params"]

    if action not in TASK_MAPPING:
        raise ValueError("Unknown task")
    
    return TASK_MAPPING[action](**params)
