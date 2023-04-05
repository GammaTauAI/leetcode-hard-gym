import leetcode
import ast
from .environment import LeetCodeEnv

env = LeetCodeEnv()

def id_from_slug(slug: str) -> str:
    """
    Retrieves the frontend id of the question with the given slug
    """
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