import json
import time
import requests
from bs4 import BeautifulSoup

def get_question(url):
    """
    Get the question page
    """
    while True:
        res = requests.get(url) # type: ignore
        status = res.status_code
        if status == 200:
            return res
        elif status == 404:
            return None
        else:
            print(status)
            time.sleep(300)
    
def title_slug(title):
    """
    Format the title into a title slug
    """
    return '-'.join(title.lower().split())

def get_code_snippets(url):
    """
    Gets the code snippets for the given question url
    """
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
    