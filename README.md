# Leetcode-Hard Gym
RL environment interface to LeetCode's submission server for evaluating codegen agents. Built on top of OpenAI's [gym](https://github.com/openai/gym).

Written by: [Beck Labash](https://github.com/becklabs)

Supports:
  - `c`
  - `c#`
  - `java`
  - `python`
  - `javascript`
  - `ruby`
  - `swift`
  - `go`
  - `scala`
  - `kotlin`
  - `rust`
  - `php`
  - `typescript`
  - `racket`
  - `erlang`
  - `elixir`
  - `dart`
  - `mysql`

### Leaderboard for Leetcode Hard (Python): Pass@1
  - OpenAI's GPT-4: `10.7` ([source](https://arxiv.org/pdf/2303.12712.pdf))
  - OpenAI's Codex: `3.6` ([source](https://arxiv.org/pdf/2303.12712.pdf))
  - OpenAI's GPT-3.5: `0.0` ([source](https://arxiv.org/pdf/2303.12712.pdf))
  - Reflexion + GPT-4: `15.0` ([source](https://arxiv.org/abs/2303.11366))

### Setup:
1. Clone the repository:
```bash
git clone https://github.com/GammaTauAI/leetcode-hard-gym.git && cd leetcode-hard-gym
```

2. Create a virtual environment and install the `leetcode_env` module and its dependencies:
```bash
python -m venv venv
source venv/bin/activate
python -m pip install -e .
```

3. Set the environment variable `LEETCODE_SESSION` to the cookie `LEETCODE_SESSION` from a signed-in Leetcode session. This cookie can be found by using browser DevTools or by using a browser extension like [EditThisCookie](https://www.editthiscookie.com/).
```bash
export LEETCODE_SESSION=...
```

### Example usage:
First we write some code:

```python
code = """
class Solution:
    def twoSum(self, nums, target):
        l = len(nums)
        for i in range(l - 1):
            for j in range(i + 1, l):
                if nums[i] + nums[j] == target:
                    return [i, j]
"""
```

Then we can build a submission ...

```python
from leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage
sub = LeetCodeSubmission(code=code,
                         lang=ProgrammingLanguage.PYTHON3,
                         question_slug='two-sum',
                         timeout=5)
```

... and instantiate a submission environment  ...

```python
from leetcode_env.environment import LeetcodeEnv
env = LeetcodeEnv()
```

Finally, we can step through the environment with the submission:

```python
status, reward, done, submission_result = env.step(sub)
print(status, reward, done, submission_result)
# Wrong Answer
# False
# False
# {'status_code': 11, 'lang': 'python3', 'run_success': True, 'status_runtime': 'N/A', 'memory': 14160000, 'question_id': '4', 'elapsed_time': 105, 'compare_result': '00010000000...00000000001000', 'code_output': '1.00000', 'std_output': '', 'last_testcase': '[1,3]\n[2]', 'expected_output': '2.00000', 'task_finish_time': 1680132323596, 'total_correct': 6, 'total_testcases': 2094, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python3', 'submission_id': '924506780', 'input_formatted': '[1,3], [2]', 'input': '[1,3]\n[2]', 'status_msg': 'Wrong Answer', 'state': 'SUCCESS'}
```

Note: compare result was shortened here, it contains a sequence of booleans indicating if a test was passed

### Cite

This benchmark was introduced in the following paper:

```bibtex
@misc{shinn2023reflexion,
      title={Reflexion: Language Agents with Verbal Reinforcement Learning}, 
      author={Noah Shinn and Federico Cassano and Beck Labash and Ashwin Gopinath and Karthik Narasimhan and Shunyu Yao},
      year={2023},
      eprint={2303.11366},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
