import ast
import re
from abc import ABC, abstractmethod
import os
import astunparse
import leetcode
# import dotenv

# dotenv.load_dotenv()

# configuration = leetcode.Configuration()

# leetcode_session = os.environ["LEETCODE_SESSION"]
# csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

# configuration.api_key["x-csrftoken"] = csrf_token
# configuration.api_key["csrftoken"] = csrf_token
# configuration.api_key["LEETCODE_SESSION"] = leetcode_session
# configuration.api_key["Referer"] = "https://leetcode.com"
# configuration.debug = False

# api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

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


class SubmissionFormatter(ABC):
    """
    Class that converts between HumanEval and Leetcode submission formats.
    """
    @abstractmethod
    def to_leetcode(self, humaneval_snippet: str):
        """
        Convert the string to leetcode format
        """
    
    @abstractmethod
    def to_humaneval(self, leetcode_snippet: str):
        """
        Convert the string to humaneval format
        """

class PySubmissionFormatter:
    @staticmethod
    def extract_comments(source: str) -> str:
        comments = re.findall(r"^\s*#.*", source, re.MULTILINE)
        return "\n".join(comments)

    @staticmethod
    def to_humaneval(leetcode_snippet: str) -> str:
        comments = PySubmissionFormatter.extract_comments(leetcode_snippet)
        try:
            tree = ast.parse(leetcode_snippet)
        except IndentationError:
            class_source = leetcode_snippet.strip() + "\n        pass"
            tree = ast.parse(class_source)
        func_node = tree.body[0].body[0]
        func_node.args.args.pop(0)  # Remove 'self' argument

        if isinstance(func_node.body[-1], ast.Pass):
            func_node.body.pop()

        new_tree = ast.Module(body=[func_node], type_ignores=[])
        return f"{comments}\n{astunparse.unparse(new_tree).strip()}\n"

    @staticmethod
    def to_leetcode(humaneval_snippet: str, class_name: str = "Solution") -> str:
        comments = PySubmissionFormatter.extract_comments(humaneval_snippet)
        try:
            tree = ast.parse(humaneval_snippet)
        except IndentationError:
            function_source = humaneval_snippet.strip() + "\n    pass"
            tree = ast.parse(function_source)

        func_node = tree.body[0]

        if isinstance(func_node.body[-1], ast.Pass):
            func_node.body.pop()

        # Add 'self' argument back to the function
        self_arg = ast.arg(arg="self", annotation=None)
        func_node.args.args.insert(0, self_arg)
        class_node = ast.ClassDef(
            name=class_name,
            bases=[],
            keywords=[],
            body=[func_node],
            decorator_list=[],
        )
        new_tree = ast.Module(body=[class_node], type_ignores=[])
        return f"{comments}\n{astunparse.unparse(new_tree).strip()}\n"

class RsSubmissionFormatter:
    @staticmethod
    def extract_comments(source: str) -> str:
        comments = re.findall(r"//.*", source)
        return "\n".join(comments)

    @staticmethod
    def to_humaneval(leetcode_snippet: str) -> str:
        comments = RsSubmissionFormatter.extract_comments(leetcode_snippet)
        function_source = re.sub(r"//.*", "", leetcode_snippet)
        function_source = re.sub(r"impl Solution \{", "", function_source)
        function_source = re.sub(r"\}", "", function_source)
        function_source = function_source.strip()
        function_source = re.sub(r"pub ", "", function_source)
        return f"{comments}\n{function_source}\n"

    @staticmethod
    def to_leetcode(humaneval_snippet: str, struct_name: str = "Solution") -> str:
        function_source = re.sub(r"//.*", "", humaneval_snippet)
        function_source = function_source.strip()
        function_source = re.sub(r"fn ", "pub fn ", function_source)
        return f"impl {struct_name} {{\n    {function_source}\n}}\n"
    