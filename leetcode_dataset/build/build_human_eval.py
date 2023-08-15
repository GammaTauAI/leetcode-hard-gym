# %% [markdown]
# ### Notebook for transforming the dataset to mimic HumanEval

# %%
import pandas as pd
import re
import json

from leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter, metadata_from_slug
from leetcode_env.environment import LeetCodeEnv

from ast import literal_eval

# %%
def to_jsonl(dict_data, file_path):
    with open(file_path, 'a') as file:
        json_line = json.dumps(dict_data)
        file.write(json_line + os.linesep)

# %%
data = pd.read_csv('data/with_snippets/leetcode_hard_with_snippets_uncontaminated_cleaned_tests.csv')
# sample = data.sample(100, random_state=1337)

# %%
data['example_test_cases'] = data['example_test_cases'].apply(literal_eval)

# %% [markdown]
# ### Python Dataset

# %%
function_name_regex = r"(?<=def\s)\w+"
lines = []

for ind, row in data.iterrows():
    task_id = row['question_slug']
    description = '\n    '.join(row['description'].strip().split('\n')).strip()
    #descripton = description.strip().replace('\n', '\n        ')
    docstring = f'''    """
    {description}
    """'''
    prompt = PySubmissionFormatter.to_humaneval(row['python3_snippet']).strip('\n') + '\n' + docstring + '\n'
    print(prompt)
    entry_point = re.search(function_name_regex, row['python3_snippet']).group(0)

    visible_tests = []
    for kwargs, expected in row['example_test_cases']:
        kwargs = {k: v.replace('null', 'None').replace('true', 'True').replace('false', 'False').replace('rue','True') for k, v in kwargs.items()}
        kwargs = ', '.join([f'{v}' for k, v in kwargs.items()])
        test = f'''assert {entry_point}({kwargs}) == {expected}'''
        visible_tests.append(test)
    
    line = {
        'task_id': task_id,
        'prompt': prompt,
        'entry_point': task_id,
        'cannonical_solution': '',
        'test': '',
        'visible_tests': visible_tests
    }
    
    lines.append(line)


# %%
for dict_data in lines:
        to_jsonl(dict_data, 'data/humaneval/leetcode-hard-py-40-uncontaminated_tests.jsonl')

# %% [markdown]
# ### Rust Dataset

# %%
from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# %%
chat = ChatOpenAI(temperature=0, model_name='gpt-4', openai_api_key='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')

# %%
is_null = False
function_name_regex = r"(?<=fn\s)\w+"
lines = []

for ind, row in data.iterrows():
    task_id = row['question_slug']
    comment = "\n".join([f"// {s}" for s in row['description'].strip().split("\n")])
    unformatted = comment + '\n' + row['rust_snippet']
    prompt = RsSubmissionFormatter.to_humaneval(comment + '\n' + row['rust_snippet']).strip('\n') + '\n'

    entry_point = re.search(function_name_regex, row['rust_snippet']).group(0)

    visible_tests = []
    for kwargs, expected in row['example_test_cases']:
        for k, v in kwargs.items():
            if 'null' in v:
                is_null = True
                print('null')
        kwargs = {k: v.replace('null', 'None').replace('true', 'True').replace('false', 'False').replace('rue','True') for k, v in kwargs.items()}
        kwargs = ', '.join([f'{v}' for k, v in kwargs.items()])
        test = f'''assert_eq!({entry_point}({kwargs}), {expected});'''
        visible_tests.append(test)
    visible_tests_old = visible_tests
    visible_tests_str = '\n'.join(visible_tests)

    messages = [
    SystemMessage(content="You are RustGPT, a rust programming assistant that accepts a list of rust test case(s), and corrects any syntactic errors they may have. Do not change the values of the test cases. Respond only with the test cases separated by a newline."),
    HumanMessage(content=f'{visible_tests_str}')
    ]

    visible_tests = chat(messages).content.split('\n')

    print(visible_tests_old)
    print(visible_tests)

    
    line = {
        'task_id': task_id,
        'prompt': prompt,
        'entry_point': task_id,
        'cannonical_solution': '',
        'test': '',
        'visible_tests': visible_tests

    }
    if is_null:
        is_null = False
        continue
    lines.append(line)

# %%
len(lines)

# %%
for dict_data in lines:
        to_jsonl(dict_data, 'data/humaneval/leetcode-hard-rs-40-uncontaminated_tests.jsonl')


