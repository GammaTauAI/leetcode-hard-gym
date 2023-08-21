import ast
import leetcode

def id_from_slug(slug: str, api_instance) -> str:
    """
    Retrieves the id of the question with the given slug
    """
    graphql_request = leetcode.GraphqlQuery(
      query="""
                  query getQuestionDetail($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                      questionId
                    }
                  }
              """,
              variables={"titleSlug": slug},
              operation_name="getQuestionDetail",
      )
    response = ast.literal_eval(str(api_instance.graphql_post(body=graphql_request)))
    frontend_id = response['data']['question']['question_id']
    return frontend_id

def metadata_from_slug(slug: str, api_instance) -> str:
    """
    Retrieves the metadata of the question with the given slug
    """
    graphql_request = leetcode.GraphqlQuery(
      query="""
                  query getQuestionDetail($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                      metaData
                    }
                  }
              """,
              variables={"titleSlug": slug},
              operation_name="getQuestionDetail",
    )
    response = ast.literal_eval(str(api_instance.graphql_post(body=graphql_request)))
    metadata = response['data']['question']
    return metadata
