import os
import json
import openai
from players.prompt_builder import build_prompt

openai.api_key = os.environ["OPENAI_API_KEY"]

class LLMAdvisor:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def analyze(self, round_state, hole_card, position, valid_actions):
        prompt = build_prompt(round_state, hole_card, position, valid_actions)

        res = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        text = res["choices"][0]["message"]["content"]
        return json.loads(text)

