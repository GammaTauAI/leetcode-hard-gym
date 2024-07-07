# Leetcode-Hard Gym
RL environment interface to LeetCode's submission server for evaluating codegen agents. Built on top of OpenAI's [gym](https://github.com/openai/gym).

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

3. Set the environment variables `LEETCODE_SESSION` to the cookie `LEETCODE_SESSION` and `LEETCODE_CSRF_TOKEN` to the cookie `csrftoken` from a signed-in Leetcode session. This cookie can be found by using browser DevTools or by using a browser extension like [EditThisCookie](https://www.editthiscookie.com/).
```bash
export LEETCODE_SESSION=...
export LEETCODE_CSRF_TOKEN=...
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

## LeetcodeHardGym Dataset

A script is provided to build an uncontaminated set of free Leetcode Hard problems in a format similar to HumanEval. It fetches the dataset, filters out class-dependent, void, and class implementation problems, and formats the problems for the specified programming languages. Optionally, it can extract test cases from examples in problem descriptions using GPT, or remove these examples from generated docstrings.

### Usage

To build the dataset, `leetcode_env` must be installed in the current environment. Then, we can run the following command from the `leetcode_dataset/` directory of this repository:
```bash
python build.py --langs python3 rust --log_level INFO --output_dir ./build
```

### Arguments

- `--langs`: List of languages. Current options are: rust, python3.
- `--log_level`: Logging level. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is INFO.
- `--output_dir`: Directory to save the built dataset. Default is ./build.
- `--extract_test_cases`: If set, test cases will be extracted from problem descriptions using GPT.
- `--remove_examples`: If set, examples will be removed. Cannot be used with --extract_test_cases.

### Environment Variables

- `LEETCODE_SESSION`: This environment variable must be set for the script to run. Please refer to the Setup section for instructions on how to obtain your session cookie. 
- `LEETCODE_CSRF_TOKEN`: This environment variable must be set for the script to run. Please refer to the Setup section for instructions on how to obtain your csrf token.
- `OPENAI_API_KEY`: This environment variable is required if the `--extract_test_cases` option is used. Please refer to the OpenAI API documentation for instructions on how to obtain your API key.

### Dependencies

If the `--extract_test_cases` option is used, the `openai` and `langchain` libraries are required. These can be installed with:
```python
 pip3 install openai langchain termcolor
```

### Output

The script will output a .jsonl file for each specified language in the output directory. The filename will be in the format `leetcode-hard-uncontaminated-{lang}.jsonl`.

### Cite

This benchmark was introduced in the following paper:

```bibtex
@misc{shinn2023reflexion,
      title={Reflexion: Language Agents with Verbal Reinforcement Learning}, 
      author={Noah Shinn and Federico Cassano and Edward Berman and Ashwin Gopinath and Karthik Narasimhan and Shunyu Yao},
      year={2023},
      eprint={2303.11366},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
