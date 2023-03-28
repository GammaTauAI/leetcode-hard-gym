import gym
import os
import leetcode
import leetcode.auth
import dotenv
import time

from pydantic import BaseModel
class LeetCodeSubmission(BaseModel):
    code: str
    lang: str
    question_id: str
    question_slug: str

dotenv.load_dotenv()

class LeetCodeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(LeetCodeEnv, self).__init__()
        self.__configure_leetcode()

    def __configure_leetcode(self):
        configuration = leetcode.Configuration()

        # From Dev Tools/Application/Cookies/LEETCODE_SESSION
        leetcode_session = os.environ["LEETCODE_SESSION"]
        csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

        configuration.api_key["x-csrftoken"] = csrf_token
        configuration.api_key["csrftoken"] = csrf_token
        configuration.api_key["LEETCODE_SESSION"] = leetcode_session
        configuration.api_key["Referer"] = "https://leetcode.com"
        configuration.debug = False

        self.api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    def step(self, action: LeetCodeSubmission):

        submission_result = self.__send_submission(action)

        reward, status = self.__calculate_reward(submission_result)

        self.reward = reward

        done = self.is_done()

        return status, reward, done, submission_result

    def reset(self):
        self.reward = False

    def __send_submission(self, sub: LeetCodeSubmission):
        submission = leetcode.Submission(
            judge_type="large", typed_code=sub.code, question_id=sub.question_id, test_mode=False, lang=sub.lang
        )

        submission_id = self.api_instance.problems_problem_submit_post(
            problem=sub.question_slug, body=submission
        )

        time.sleep(5)

        submission_result = self.api_instance.submissions_detail_id_check_get(
            id=submission_id.submission_id
        )

        return submission_result

    def __calculate_reward(self, submission_result):
        status_msg = submission_result['status_msg'] # 'Accepted' | 'Runtime Error'| 'Wrong Answer'
        return status_msg == 'Accepted', status_msg
    
    def is_done(self):
        return self.reward

