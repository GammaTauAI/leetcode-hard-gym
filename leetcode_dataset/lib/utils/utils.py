import json
import time
import requests
from bs4 import BeautifulSoup
import os
from typing import List
import leetcode
import leetcode.auth
from typing import Dict
import string

def lines_to_jsonl(lines: List[Dict], file_path: str):
    """
    Convert a list of dicts to a jsonl file
    """
    # Empty the current file
    open(file_path, 'w').close()

    with open(file_path, 'a') as file:
        for dict_data in lines:
            json_line = json.dumps(dict_data)
            file.write(json_line + os.linesep)

def get_api_instance():
    """
    Get the leetcode api instance
    """
    configuration = leetcode.Configuration()

    # From Dev Tools/Application/Cookies/LEETCODE_SESSION
    leetcode_session = os.environ["LEETCODE_SESSION"]
    csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

    configuration.api_key["x-csrftoken"] = csrf_token
    configuration.api_key["csrftoken"] = csrf_token
    configuration.api_key["LEETCODE_SESSION"] = leetcode_session
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    return api_instance

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

def slug_to_title(question_slug: str) -> str:
    """Format a Leetcode question's slug as a title"""
    return string.capwords(question_slug.replace("-", " ")).strip()

def format_integer(n):
    """Format the integer to have a length of 4 by padding with zeroes."""
    return str(n).zfill(4)[:4]

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

url = "https://leetcode.com/graphql/"

payload = lambda slug: json.dumps({
  "query": "\n    query consolePanelConfig($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    exampleTestcaseList\n  }\n}\n    ",
  "variables": {
    "titleSlug": slug
  },
  "operationName": "consolePanelConfig"
})

headers = {
  'authority': 'leetcode.com',
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'authorization': '',
  'baggage': 'sentry-environment=production,sentry-release=8f466f72,sentry-transaction=%2Fproblems%2F%5Bslug%5D%2F%5B%5B...tab%5D%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=897972800d1c46e5a5d499f12244a91b,sentry-sample_rate=0.004',
  'content-type': 'application/json',
  'cookie': 'gr_user_id=35b498db-f28f-485f-8b44-417f8fba15ed; __stripe_mid=04d7a882-553c-499c-8866-bcf56aac8ef6ed918f; __atuvc=1%7C5; NEW_PROBLEMLIST_PAGE=1; csrftoken=9BiGVDJiJS7iFJKVYZ1CNMNulRAvYUdlezUlp1oYOrsR2zVsk9mZh1MD6C2d6twV; messages="9b526d67f2587ca52e83b4431db91f6bd6abdac1$[[\\"__json_message\\"\\0540\\05425\\054\\"You have signed out.\\"]\\054[\\"__json_message\\"\\0540\\05425\\054\\"Successfully signed in as beckles168.\\"]\\054[\\"__json_message\\"\\0540\\05425\\054\\"You have signed out.\\"]\\054[\\"__json_message\\"\\0540\\05425\\054\\"Successfully signed in as leetcodeexecutor.\\"]\\054[\\"__json_message\\"\\0540\\05425\\054\\"You have signed out.\\"]\\054[\\"__json_message\\"\\0540\\05425\\054\\"Successfully signed in as beckles168.\\"]]"; 87b5a3c3f1a55520_gr_last_sent_cs1=beckles168; _gid=GA1.2.2067840721.1681477917; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiOTIwNjcxMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjU2MGIwZGIzMjVjOTcwNTk3OGFkZDI4MjY0MzM5NjU0NzVjZDhmMjYiLCJpZCI6OTIwNjcxMywiZW1haWwiOiJiZWNrbGVzMTY4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYmVja2xlczE2OCIsInVzZXJfc2x1ZyI6ImJlY2tsZXMxNjgiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY4MDY1MjE2OC5wbmciLCJyZWZyZXNoZWRfYXQiOjE2ODE2NjIzMDAsImlwIjoiNzIuMTk1LjEzNC4zMSIsImlkZW50aXR5IjoiNzIzYzUxMjYzYzgwZjZiZTc5ZmEyMTE5MWVlMGIzODciLCJzZXNzaW9uX2lkIjozNzg5MzIzNH0.BJV_u27JVniHZ73kI76oTTkFGK4OHNJPpv-F58pZBUc; 87b5a3c3f1a55520_gr_session_id=73357b2f-2c35-49f4-8256-556aa503d604; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=73357b2f-2c35-49f4-8256-556aa503d604; 87b5a3c3f1a55520_gr_session_id_73357b2f-2c35-49f4-8256-556aa503d604=true; _gat=1; 87b5a3c3f1a55520_gr_cs1=beckles168; _ga=GA1.1.1043183799.1675086637; __stripe_sid=d8eb8303-f932-4cfd-92ef-9ed80b781cae827bea; _ga_CDRWKZTDEX=GS1.1.1681662302.39.1.1681665678.0.0.0; _dd_s=rum=0&expire=1681666578197; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiOTIwNjcxMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjU2MGIwZGIzMjVjOTcwNTk3OGFkZDI4MjY0MzM5NjU0NzVjZDhmMjYiLCJpZCI6OTIwNjcxMywiZW1haWwiOiJiZWNrbGVzMTY4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYmVja2xlczE2OCIsInVzZXJfc2x1ZyI6ImJlY2tsZXMxNjgiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY4MDY1MjE2OC5wbmciLCJyZWZyZXNoZWRfYXQiOjE2ODE2NjIzMDAsImlwIjoiNTQuODYuNTAuMTM5IiwiaWRlbnRpdHkiOiI3MjNjNTEyNjNjODBmNmJlNzlmYTIxMTkxZWUwYjM4NyIsInNlc3Npb25faWQiOjM3ODkzMjM0fQ.DtQ8KCL7Qsua4Bp-vOMJfg4VJUjX4NSxhdNXs756x4M; csrftoken=9BiGVDJiJS7iFJKVYZ1CNMNulRAvYUdlezUlp1oYOrsR2zVsk9mZh1MD6C2d6twV',
  'origin': 'https://leetcode.com',
  'random-uuid': '4922dfe3-8c3c-1d65-9b7a-ca84bfe9f756',
  'referer': 'https://leetcode.com/problems/two-sum/',
  'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sentry-trace': '897972800d1c46e5a5d499f12244a91b-a37933a4a1d212e3-0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'x-csrftoken': '9BiGVDJiJS7iFJKVYZ1CNMNulRAvYUdlezUlp1oYOrsR2zVsk9mZh1MD6C2d6twV'
}

def test_cases_from_slug(slug: str) -> List[str]:
    response = requests.post(url, headers=headers, data=payload(slug))
    return dict(response.json())['data']['question']['exampleTestcaseList']

