import pandas as pd
import time
import sys
import ast
import re
sys.path.append('..')
from .utils import test_cases_from_slug
import re

def extract_examples(description):
    inputs = [l for l in description.split('\n') if l.startswith('Input')]
    outputs = [l.strip('Output: ') for l in description.split('\n') if l.startswith('Output')]

    examples = []

    for input_str, output_str in zip(inputs, outputs):
        kwargs_str = re.sub(r'\s+', '', input_str)
        kwargs_pairs = re.findall(r"(\w+)\s*=\s*([-\w\[\],]+)(?:,|$)", kwargs_str)
        kwargs = {k: v for k, v in kwargs_pairs}
        output = output_str
        examples.append((kwargs, output))

    return examples


def add_test_cases(data: pd.DataFrame, lang: str = 'python') -> pd.DataFrame:
    data['example_test_cases'] = None
    for ind, row in data.iterrows():
        print(ind)
        examples = extract_examples(row['description'])
        data.at[ind, 'example_test_cases'] = examples

    data.to_csv('data/with_snippets/leetcode_hard_with_snippets_uncontaminated_tests.csv')

data['example_test_cases'] = None
for ind, row in data.iterrows():
    print(ind)
    slug = row['question_slug']
    test_cases = test_cases_from_slug(slug)
    data.at[ind, 'example_test_cases'] = test_cases
    time.sleep(5)

data.iloc[6]['example_test_cases']

function_name_regex = r"(?<=def\s)\w+"
no_args = 0
data['example_test_cases_parsed'] = None
for ind, row in data.iterrows():
    statements = []
    for test in row['example_test_cases']:
        args = test.split('\n')[:-1]
        if len(args) == 0:
            no_args += 1
        expected_val = test.split('\n')[-1]
        entry_point = re.search(function_name_regex, row['python3_snippet']).group(0)
        statement = f"assert {entry_point}({', '.join(args)}) == {expected_val}"
        statements.append(statement)
    #print(statements)
    data.at[ind, 'example_test_cases_parsed'] = statements
print(no_args)

da.to_csv('data/with_snippets/leetcode_hard_with_snippets_uncontaminated_cleaned_tests.csv')


