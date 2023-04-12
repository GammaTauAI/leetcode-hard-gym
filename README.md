# Leetcode-Hard Gym
A gym to evaluate superhuman programming agents built on top of OpenAI's [gym](https://github.com/openai/gym).

Written by: [Beck Labash](https://github.com/becklabs)

Supports:
  - `python`
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
  - Reflexion + GPT-4: `???`

### Setup:

  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt

- Set environment variable `LEETCODE_SESSION` to the cookie `LEETCODE_SESSION` from a signed-in Leetcode session or set it in the .env file


### Basic Usage

```python

from leetcode_hard_gym.main import run_all

# define `generate_one_completion` to be a function that generates code
def generate_one_completion(prompt):
    return "def hello_world():\n    print('hello world')"

run_gym(
  generate_one_completion,
  output_file="results.jsonl",
  lang="python3"
)
```

### Detailed Example usage:

We can load the code-snippet annotated dataset like so:

```python
import pandas as pd
data = pd.read_csv("path/to/repo/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets.csv")
row = data.iloc[0]
```

Then we can instantiate a submission environment ...
```python
from leetcode_hard_gym.leetcode_env.environment import LeetCodeEnv

env = LeetCodeEnv()
```

... and build a submission using a row from the dataset ...

```python
from leetcode_hard_gym.leetcode_env.leetcode_types import LeetCodeSubmission

code = """
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        return 1
"""
lang = "python3"
question_id = row['id']
question_slug = row['title_slug']

sub = LeetCodeSubmission(code=code,
                         lang=lang,
                         question_id=question_id,
                         question_slug=question_slug
                         timeout = 5)
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

