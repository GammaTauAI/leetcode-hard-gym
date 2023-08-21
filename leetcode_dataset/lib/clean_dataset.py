import pandas as pd
import re

def remove_class_dependent(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Remove problems that depend on class definitions
    """
    dataset = dataset.copy()
    no_defs_inds = [ind for ind, row in dataset.iterrows() if row['cpp_snippet'].split(' ')[0] == 'class']
    no_defs = dataset.iloc[no_defs_inds]
    return no_defs

def remove_void(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Remove problems that request a void implementation
    """
    dataset = dataset.copy()
    ret_inds = [ind for ind, row in dataset.iterrows() if '\"\"\"' in row['python3_snippet'].split('\n')[2]]
    ret = dataset.drop(ret_inds)
    return ret

def remove_class_impls(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Remove problems that request a class implementation
    """
    dataset = dataset.copy()
    function_name_regex = r"(?<=def\s)\w+"
    impl_inds = [ind for ind, row in dataset.iterrows()
             if re.search(function_name_regex, row['python3_snippet']).group(0) == '__init__']
    no_impl = dataset.drop(impl_inds)
    return no_impl

def remove_examples(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of the dataset without examples in the descriptions
    """
    dataset = dataset.copy()
    for ind, row in dataset.iterrows():
        res = docstring_remove_empty(docstring_remove_examples(row['description']))
        dataset.at[ind, 'description'] = res

    return dataset

def docstring_remove_examples(docstring: str):
    """
    Remove the examples from the docstring 
    """
    lines = [l.strip() for l in docstring.split('\n')]
    for i, line in enumerate(lines):
        if 'Example' in line:
            return '\n'.join(lines[:i])
    return docstring

def docstring_remove_empty(desc: str):
    """
    Remove empty lines from the docstring
    """
    return '\n'.join(line for line in desc.split('\n') if line.strip())



