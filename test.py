from environment import LeetCodeEnv, LeetCodeSubmission

code = """
class Solution:
    def twoSum(self, nums, target):
        return [0]
"""
lang = "python"
question_id = 1
question_slug = 'two-sum'

sub = LeetCodeSubmission(code=code,
                         lang=lang,
                         question_id=question_id,
                         question_slug=question_slug)

env = LeetCodeEnv()

env.step(sub)

