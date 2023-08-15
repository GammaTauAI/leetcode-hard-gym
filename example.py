from leetcode_env.environment import LeetCodeEnv
from leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage

code = """
class Solution:
    def twoSum(self, nums, target):
        l = len(nums)
        for i in range(l - 1):
            for j in range(i + 1, l):
                if nums[i] + nums[j] == target:
                    return [i, j]
"""

sub = LeetCodeSubmission(code=code,
                         lang=ProgrammingLanguage.PYTHON3,
                         question_slug='two-sum')

env = LeetCodeEnv()

status, reward, done, submission_result = env.step(sub)

print(status, reward, done, submission_result)

