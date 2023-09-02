import dotenv
import pandas as pd
import ast
from bs4 import BeautifulSoup
import time
import leetcode
import logging
import html2text
import re

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True  

dotenv.load_dotenv()

def get_info(question_slug: str, api_instance):
    """
    Retrieves the metadata of the question with the given slug
    """
    graphql_request = leetcode.GraphqlQuery(
    query="""
                query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    codeSnippets {
                        lang
                        langSlug
                        code
                        __typename
                    }
                    content
                    title 
                }
                }
            """,
            variables={"titleSlug": question_slug},
            operation_name="getQuestionDetail",
)
    response = ast.literal_eval(str(api_instance.graphql_post(body=graphql_request)))
    data = response['data']['question']
    return data 

def fetch_dataset(api_instance):
    """
    Get the hard, free, uncontaminated, hard questions from the algorithms topic  
    """
    question_infos = api_instance.api_problems_topic_get(topic="algorithms")
    logging.info(f"Fetched question infos")

    hard = [q for q in question_infos.stat_status_pairs
            if q.difficulty.level == 3
            and q.paid_only == False]

    hard_dicts = [q.to_dict() for q in hard]

    slug = 'paths-in-matrix-whose-sum-is-divisible-by-k' # This is the first uncontaminated problem
    index = next((i for i, q in enumerate(hard_dicts) if q['stat']['question__title_slug'] == slug), None)
    uncontaminated = hard[:index + 1]
    uncontaminated = uncontaminated[-41:] # Need to get the oldest 41 problems so that the benchmark is consistent

    df = pd.DataFrame()
    for ind, question in enumerate(uncontaminated):
        logging.info(f"Fetching code snippets for problem {ind + 1}/{len(uncontaminated)}")
        question_slug = question.stat.question__title_slug
        info = get_info(question_slug, api_instance)
        snippets = info['code_snippets']
        content = BeautifulSoup(info['content'], features='html.parser')
        text_content = h.handle(str(content))
        text_content = "\n".join(line.lstrip() for line in text_content.split("\n"))
        text_content = re.sub('\n\n+', '\n\n', text_content)
        text_content = text_content.strip().strip('\n')

        df.at[ind, "question_slug"] = question.stat.question__title_slug
        df.at[ind, "question_title"] = question.stat.question__title
        df.at[ind, "frontend_question_id"] = int(question.stat.frontend_question_id)
        df.at[ind, "question_id"] = int(question.stat.question_id)
        df.at[ind, "description"] = text_content  

        for snippet in snippets:
            df.at[ind, snippet['lang_slug'] + '_snippet'] = snippet['code']

    return df

