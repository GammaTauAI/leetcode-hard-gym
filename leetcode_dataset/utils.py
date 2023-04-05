import json
import requests
import time
from bs4 import BeautifulSoup
import requests

def get_question(slug):
    while True:
        res = requests.get(f'https://leetcode.com/problems/{slug}/')
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

def get_code_snippets(slug):
    res = get_question(slug)
    if res is None:
        return None
    soup = BeautifulSoup(res.content, "html.parser")
    script_tag = soup.find('script', {'type': 'application/json'})
    data = dict(json.loads(script_tag.string))
    queries = data['props']['pageProps']['dehydratedState']['queries']
    query = [i for i in queries if 'question' in i['state']['data'] and 'codeSnippets' in i['state']['data']['question']][0]
    code_snippets = query["state"]["data"]["question"]["codeSnippets"]
    return code_snippets

env = LeetCodeEnv()

def id_from_slug(slug: str) -> str:
  graphql_request = leetcode.GraphqlQuery(
          query="""
              query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                  questionFrontendId
                }
              }
          """,
          variables={"titleSlug": slug},
          operation_name="getQuestionDetail",
  )
  response = ast.literal_eval(str(env.api_instance.graphql_post(body=graphql_request)))
  frontend_id = response['data']['question']['question_frontend_id']

  return frontend_id

