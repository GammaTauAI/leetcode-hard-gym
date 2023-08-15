import pandas as pd
import re
from leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter

def remove_examples(desc):
    lines = [l.strip() for l in desc.split('\n')]
    for i, line in enumerate(lines):
        if 'Example' in line:
            return '\n'.join(lines[:i])
    return desc

def remove_empty(desc: str):
    return '\n'.join(line for line in desc.split('\n') if line.strip())

def clean_dataset(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    no_defs_inds = [ind for ind, row in data.iterrows() if row['cpp_snippet'].split(' ')[0] == 'class']
    no_defs = data.iloc[no_defs_inds]

    ret_inds = [ind for ind, row in no_defs.iterrows() if '\"\"\"' in row['python3_snippet'].split('\n')[2]]
    ret = no_defs.drop(ret_inds)

    function_name_regex = r"(?<=def\s)\w+"
    impl_inds = [ind for ind, row in no_defs.iterrows()
             if re.search(function_name_regex, row['python3_snippet']).group(0) == '__init__']
    no_impl = ret.drop(impl_inds)

    for ind, row in no_impl.iterrows():
        res = remove_empty(remove_examples(row['description']))
        no_impl.at[ind, 'description'] = res

    return no_impl


