import logging
import os

import openai

log = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("Could not find OPENAI_API_KEY in environment variables")

openai.api_key = OPENAI_API_KEY


class PromptManager:
    def __init__(self, model="gpt-4"):
        self.messages = []
        self.model = model

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def generate(self):
        res = openai.ChatCompletion.create(
            model=self.model, messages=self.messages, temperature=0.2
        )
        content = res["choices"][0]["message"]["content"]
        log.info("Prompt result: %s", content)
        self.add_message(role="assistant", content=content)
        return content
