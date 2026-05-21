import json
import os
import re

from google import genai


class GeminiAdvisor:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"]
        )

    def analyze(self, round_state, hole_card, position, valid_actions):

        from players.prompt_builder import build_prompt

        prompt = build_prompt(
            round_state,
            hole_card,
            position,
            valid_actions
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        try:

            # ===== EXTRACT JSON =====

            match = re.search(r'\{.*\}', text, re.DOTALL)

            if not match:
                raise ValueError("No JSON found")

            parsed = json.loads(match.group())

            return parsed

        except Exception as e:

            print("Gemini raw:", text)
            print("Parse error:", e)

            return {
                "action": "call",
                "amount": 0
            }
