import json
import os
import re

import anthropic


class ClaudeAdvisor:

    def __init__(self):

        self.client = anthropic.Anthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    def analyze(self, round_state, hole_card, position, valid_actions):

        from players.prompt_builder import build_prompt

        prompt = build_prompt(
            round_state,
            hole_card,
            position,
            valid_actions
        )

        response = self.client.messages.create(

            # ===== MODEL =====
            model="claude-opus-4-7",
            max_tokens=200,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = response.content[0].text.strip()

        try:

            match = re.search(
                r'\{.*\}',
                text,
                re.DOTALL
            )

            if not match:
                raise ValueError("No JSON found")

            parsed = json.loads(match.group())

            return parsed

        except Exception as e:

            print("Claude raw:", text)
            print("Claude parse error:", e)

            return {
                "action": "call",
                "amount": 0
            }
