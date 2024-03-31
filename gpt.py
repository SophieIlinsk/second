import requests
from info import *
from confing import *


class Question_gpt2:
    def __init__(self):
        self.URL = GPT_LOCAL_URL
        self.HEADERS = HEADERS
        self.MAX_TOKENS = MAX_TOKENS

    def promt(self, result1, system_content):
        try:
            resp = requests.post(
                self.server,
                headers={"Content-Type": "application/json"},
                json={
                    "messages": [
                        {"role": "system", "content": f'{system_content}'},
                        {"role": "user", "content": f'{result1.text}'},
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
            )
            data = resp.json()
            error_gpt(resp, data)
            answer = data['choices'][0]['message']['content']
            return answer

        except Exception as e:
            error_gpt1 = error_1
            logging.error(str(e))
            return error_gpt1


class Continue_text_gpt:
    def __init__(self):
        self.URL = GPT_LOCAL_URL
        self.HEADERS = HEADERS
        self.MAX_TOKENS = MAX_TOKENS
        self.assistant = ("Continue your answer, based on the previous answers that I will now provide you, "
                     "you need to continue the answer strictly on the topic that is given in the previous answers.")

    def gpt(self, promt1, system_content):
        try:
            resp = requests.post(
                    self.server,
                    headers={"Content-Type": "application/json"},
                    json={
                        "messages": [
                            {"role": "system", "content": f'{system_content}'},
                            {"role": "assistant", "content": f'{self.assistant} {promt1}'},
                        ],
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens
                    }
                )
            data = resp.json()
            error_gpt(resp, data)
            continuation = data['choices'][0]['message']['content']
            return continuation

        except Exception as e:
            error1 = error_1
            logging.error(str(e))
            return error_2