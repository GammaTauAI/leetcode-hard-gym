from leetcode_env.environment import LeetCodeEnv
from leetcode_env.leetcode_types import LeetCodeSubmission, ProgrammingLanguage
from leetcode_env.utils import id_from_slug
code = """
class Solution:
    def twoSum(self, nums, target):
        return [0]
"""
lang = ProgrammingLanguage.PYTHON3
question_id = 1
question_slug = 'two-sum'

sub = LeetCodeSubmission(code=code,
                         lang=lang,
                         question_id=id_from_slug(question_slug),
                         question_slug=question_slug)

env = LeetCodeEnv()

status, reward, done, submission_result = env.step(sub)

print(status, reward, done, submission_result)

