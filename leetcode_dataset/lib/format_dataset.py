import pandas as pd
import logging
from .utils.utils import lines_to_jsonl
from leetcode_env.utils.formatting import (
    PythonSubmissionFormatter,
    RustSubmissionFormatter,
    SubmissionFormatter,
)

FORMATTERS = {
    "python3": PythonSubmissionFormatter,
    "rust": RustSubmissionFormatter,
}


def format_problems(dataset: pd.DataFrame, lang: str):
    """
    Convert problems to functions with their descriptsions as docstrings
    Adds columns: 'signature', 'prompt'
    """
    formatter: SubmissionFormatter = FORMATTERS.get(lang)
    dataset = dataset.copy()
    for ind, row in dataset.iterrows():
        formatted_problem = formatter.to_humaneval(row[f"{lang}_snippet"])
        prompt = formatter.add_docstring(formatted_problem, row["description"])
        signature = formatter.extract_signature(formatted_problem)
        dataset.at[ind, "signature"] =  signature
        dataset.at[ind, "prompt"] = prompt
    return dataset

def to_jsonl(dataset: pd.DataFrame, path: str):
    """
    Save the dataset to a jsonl file 
    """
    logging.info(f"Writing dataset to {path}")
    lines = []
    for ind, row in dataset.iterrows():
        task_id = row["question_slug"]
        test_cases = '\n'.join(row.get("test_cases", []))
        solution = row.get("solution", "")
        prompt = row["prompt"]
        signature = row["signature"]
        docstring = row["description"]

        line = {
            "task_id": task_id,
            "prompt": prompt,
            "canonical_solution": solution,
            "test": test_cases,
            "signature": signature,
            "docstring": docstring,
        }

        lines.append(line)

    lines_to_jsonl(lines, path)

