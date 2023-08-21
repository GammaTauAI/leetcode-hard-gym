from leetcode_env.utils.formatting import PythonSubmissionFormatter
import pytest

to_humaneval_samples = [
    ("""
class Solution:
    def some_function(self, x: int, y: int) -> int:
    """,
    """
def some_function(x: int, y: int) -> int:
    """.strip()),

    ("""
class Solution:
    def some_function(self, x: int, y: int) -> int:
        x = 1
        return (x + y)
    """,
    """
def some_function(x: int, y: int) -> int:
    x = 1
    return (x + y)
    """.strip()),
]

to_leetcode_samples = [
    ("""
def some_function(x: int, y: int) -> int:
    """.strip(),
    """
class Solution():

    def some_function(self, x: int, y: int) -> int:
    """.strip()),

    ("""
def some_function(x: int, y: int) -> int:
    x = 1
    return (x + y)
    """,
    """
class Solution():

    def some_function(self, x: int, y: int) -> int:
        x = 1
        return (x + y)
    """.strip()),

    ("""
from collections import Counter
def some_function(x: int, y: int) -> int:
    import string
    x = 1
    return (x + y)
    """,
    """
from collections import Counter
class Solution():

    def some_function(self, x: int, y: int) -> int:
        import string
        x = 1
        return (x + y)
    """.strip()),
]

@pytest.mark.parametrize("leetcode_snippet, expected", to_humaneval_samples)
def test_to_humaneval(leetcode_snippet, expected):
    result = PythonSubmissionFormatter.to_humaneval(leetcode_snippet).strip()
    assert result == expected

    # try:
    #     assert expected == result
    # except AssertionError as e:
    #     print(f"Expected:\n{expected}")
    #     print('-'*20)
    #     print(f"Result:\n{result}")
    #     raise


@pytest.mark.parametrize("humaneval_snippet, expected", to_leetcode_samples)
def test_to_leetcode(humaneval_snippet, expected):
    result = PythonSubmissionFormatter.to_leetcode(humaneval_snippet).strip()
    assert result == expected
