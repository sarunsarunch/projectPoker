import json

def build_prompt(round_state, hole_card, position, valid_actions):
    state = {
        "hole_card": hole_card,
        "position": position,
        "round_state": round_state,
        "valid_actions": valid_actions,
    }

    state_text = json.dumps(state, indent=2)

    prompt = f"""
You are a professional Texas Hold'em poker player.

Your task:
- Analyze the current game state
- Choose the BEST possible action to maximize long-term winning

IMPORTANT RULES:
- Do NOT always choose call when call amount is 0
- Passive play is DISCOURAGED
- If you have a strong hand → RAISE
- If opponents show weakness → you may BLUFF
- You are allowed to take risks if reasonable

Decision rules:
- Choose exactly ONE action
- Valid actions: {valid_actions}
- If action is "raise", amount must be reasonable
- Respond ONLY in valid JSON
- Do NOT explain outside JSON

Current game state:
{state_text}

Respond in this exact JSON format:
{{
  "action": "fold | call | raise",
  "amount": <integer>,
  "confidence": <number between 0 and 1>,
  "reason": "<short reason>"
}}
"""
    return prompt
