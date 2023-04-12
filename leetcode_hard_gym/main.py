import json

import pandas as pd
import tqdm
from leetcode_env.environment import LeetCodeEnv
from leetcode_env.leetcode_types import LeetCodeSubmission

from .leetcode_env.environment import LeetCodeEnv
from .leetcode_env.leetcode_types import (LeetCodeSubmission,
                                          ProgrammingLanguage)
from .leetcode_env.utils import id_from_slug


def load_dataset():
    return pd.read_csv(
        "./leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets.csv"
    )


def run_all(generate_one_completion: callable, output_file: str = None, lang="python3"):
    """generate_one_completion is a function that takes in a question_slug and returns an executable code snippet"""
    questions = load_dataset()
    env = LeetCodeEnv()

    ittr = tqdm.tqdm(questions.iterrows(), total=len(questions))
    for _, row in ittr:
        question_id = row["id"]
        question_slug = row["title_slug"]

        ittr.set_description(f"Running {question_slug}")
        code = generate_one_completion(question_slug)

        ittr.set_description(f"Submitting {question_slug}")
        sub = LeetCodeSubmission(
            code=code,
            lang=lang,
            question_id=question_id,
            question_slug=question_slug,
            timeout=5,
        )

        status, reward, done, submission_result = env.step(sub)
        output = dict(
            lang=lang,
            question_id=question_id,
            question_slug=question_slug,
            status=status,
            reward=reward,
            done=done,
            submission_result=submission_result,
            code=code,
        )

        with open(output_file, "a") as f:
            f.write(json.dumps(output) + "\n")
        ittr.set_description(f"Completed {question_slug}")
