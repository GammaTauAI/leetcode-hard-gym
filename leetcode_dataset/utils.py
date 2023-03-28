import json
import requests
import time
from bs4 import BeautifulSoup
import random
import requests

payload = {

}
    
user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.888",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Vivaldi/1.9.818.50",
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.888",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/15.15063",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Vivaldi/1.9.818.50",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/44.0.2510.1449",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
]
    
headers = lambda : {
  'authority': 'leetcode.com',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'gr_user_id=35b498db-f28f-485f-8b44-417f8fba15ed; 87b5a3c3f1a55520_gr_last_sent_cs1=becklabs; __stripe_mid=04d7a882-553c-499c-8866-bcf56aac8ef6ed918f; __atuvc=1%7C5; csrftoken=tqCv9COPewPJk9SMwiGedLblniBWmssbXpLzJuzmQ5NuwUmTLXep4ZBL42mzKRTe; messages="fb06277bdff36ca9729e50121f94e13f1737d17d$[[\\"__json_message\\"\\0540\\05425\\054\\"Successfully signed in as becklabs.\\"]]"; NEW_PROBLEMLIST_PAGE=1; _lr_uf_-7j19o6=2a99f1ba-3a44-4b3a-9aff-d2f1130a31cd; _gid=GA1.2.1173746001.1679538548; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNDE0NjIzNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImEwY2NiNDVjMmZlOTgxYjBhYzliZGUwYTRlMTQ0ODI2MjM0OTc0ZGMiLCJpZCI6NDE0NjIzNCwiZW1haWwiOiJiZWNrbGFiYXNoQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYmVja2xhYnMiLCJ1c2VyX3NsdWciOiJiZWNrbGFicyIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9iZWNrbGFicy9hdmF0YXJfMTYxODI0MDgzOS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2Nzk2MTc2NTksImlwIjoiMTU1LjMzLjEzMy41IiwiaWRlbnRpdHkiOiIwOGM4NmFmOWQxZTUxZWFiZGUzY2EyMGM1ZTI5MzMwOCIsInNlc3Npb25faWQiOjM2NjYwNTM5fQ.nqGjpIwFEAvYMOusWYlvqW6zYLXWdUwZ5tRc7l6c1bg; _ga=GA1.1.1043183799.1675086637; 87b5a3c3f1a55520_gr_session_id=9518494e-9943-4084-b450-b91181e5d443; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=9518494e-9943-4084-b450-b91181e5d443; 87b5a3c3f1a55520_gr_cs1=becklabs; 87b5a3c3f1a55520_gr_session_id_9518494e-9943-4084-b450-b91181e5d443=true; _ga_CDRWKZTDEX=GS1.1.1679619489.8.0.1679619489.0.0.0; __stripe_sid=319851da-5dfa-401f-b558-46633d26f6fa6b582f; _dd_s=rum=0&expire=1679620394534; csrftoken=amb5HgoIcIfrDo3sf1Dscr7qhy3iXErKtOii2BZ80fJxx6UIjVfIUa1tZUA3kULd',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': random.choice(user_agents)
}


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