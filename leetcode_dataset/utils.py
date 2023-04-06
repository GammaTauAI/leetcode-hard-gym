import json
import requests
import time
from bs4 import BeautifulSoup
import requests

def get_question(url):
    while True:
        res = requests.get(url)
        status = res.status_code
        if status == 200:
            return res
        elif status == 404:
            return None
        else:
            print(status)
            time.sleep(300)
    
def title_slug(title):
    return '-'.join(title.lower().split())

def get_code_snippets(url):
    res = get_question(url)
    if res is None:
        return None
    soup = BeautifulSoup(res.content, "html.parser")
    script_tag = soup.find('script', {'type': 'application/json'})
    data = dict(json.loads(script_tag.string))
    queries = data['props']['pageProps']['dehydratedState']['queries']
    query = [i for i in queries if 'question' in i['state']['data'] and 'codeSnippets' in i['state']['data']['question']][0]
    code_snippets = query["state"]["data"]["question"]["codeSnippets"]
    return code_snippets


import re
from abc import ABC, abstractmethod

class SubmissionFormatter(ABC):
    """
    Class that converts between HumanEval and Leetcode submission formats.
    """
    @abstractmethod
    def to_leetcode(self, humaneval_snippet: str):
        ...
    
    @abstractmethod
    def to_humaneval(self, leetcode_snippet: str):
        ...

class PySubmissionFormatter(SubmissionFormatter):
    def to_leetcode(self, humaneval_snippet: str):
        comment_pattern = re.compile(r"((?:#.*\n)*)")
        comment_match = comment_pattern.match(humaneval_snippet)
        comments = comment_match.group(1) if comment_match else ""
        
        # Remove comments from the snippet
        humaneval_snippet = comment_pattern.sub("", humaneval_snippet).strip()
        humaneval_snippet_indented = humaneval_snippet.replace('\n', '\n    ')
        
        return f"""\
{comments}class Solution:
    {humaneval_snippet_indented}
"""

    def to_humaneval(self, leetcode_snippet: str):
        comment_pattern = re.compile(r"((?:#.*\n)*)")
        comment_match = comment_pattern.match(leetcode_snippet)
        comments = comment_match.group(1) if comment_match else ""
        
        # Remove comments from the snippet
        leetcode_snippet = comment_pattern.sub("", leetcode_snippet).strip()
        
        pattern = re.compile(r"class Solution:\s+([\s\S]+)")
        match = pattern.search(leetcode_snippet)
        if match:
            return f"{comments}{match.group(1).replace('    ', '', 1)}"
        return leetcode_snippet.strip()


class RsSubmissionFormatter(SubmissionFormatter):
    def to_leetcode(self, humaneval_snippet: str):
        return f"""\
        impl Solution {{
            {humaneval_snippet.strip()}
        }}
        """

    def to_humaneval(self, leetcode_snippet: str):
        pattern = re.compile(r"impl Solution \{([\s\S]+)\}")
        match = pattern.search(leetcode_snippet)
        if match:
            return match.group(1).strip()
        return leetcode_snippet.strip()
    