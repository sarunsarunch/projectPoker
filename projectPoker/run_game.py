from pypokerengine.api.game import setup_config, start_poker

from players.llm_player import LLMPlayer
from players.llm_advisor import LLMAdvisor
from players.gemini_advisor import GeminiAdvisor
from players.claude_advisor import ClaudeAdvisor

from datetime import datetime

import pandas as pd
import os
import random

# =========================================
# REPRODUCIBILITY
# =========================================
random.seed(42)

# =========================================
# FIXED HANDS CONFIG
# =========================================
TARGET_HANDS = 1000

START_STACK = 3000

SMALL_BLIND = 10

BIG_BLIND = SMALL_BLIND * 2

# =========================================
# LOG FOLDER
# =========================================
os.makedirs("logs", exist_ok=True)

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

# =========================================
# GLOBAL TRACKER
# =========================================
total_hands_played = 0

all_results = []

# =========================================
# CREATE PLAYERS (KEEP MEMORY)
# =========================================
gpt_player = LLMPlayer(

    advisor=LLMAdvisor(),

    name="GPTBot",

    game_id="GLOBAL"
)

gemini_player = LLMPlayer(

    advisor=GeminiAdvisor(),

    name="GeminiBot",

    game_id="GLOBAL"
)

claude_player = LLMPlayer(

    advisor=ClaudeAdvisor(),

    name="ClaudeBot",

    game_id="GLOBAL"
)

# =========================================
# START FIXED HAND LOOP
# =========================================
print("\n========== START FIXED HANDS ==========\n")

for hand_id in range(1, TARGET_HANDS + 1):

    GAME_ID = f"HAND_{hand_id}"

    print(f"\n🎮 START {GAME_ID}")

    # =========================================
    # ONE HAND ONLY
    # =========================================
    config = setup_config(

        max_round=1,

        initial_stack=START_STACK,

        small_blind_amount=SMALL_BLIND
    )

    # =========================================
    # REGISTER PLAYERS
    # =========================================
    config.register_player(

        name="GPTBot",

        algorithm=gpt_player
    )

    config.register_player(

        name="GeminiBot",

        algorithm=gemini_player
    )

    config.register_player(

        name="ClaudeBot",

        algorithm=claude_player
    )

    # =========================================
    # START GAME
    # =========================================
    game_result = start_poker(
        config,
        verbose=0
    )

    # =========================================
    # EXACT HAND COUNT
    # =========================================
    total_hands_played += 1

    print(
        f"\n✅ {GAME_ID} finished"
    )

    print(
        f"Total hands : "
        f"{total_hands_played}"
    )

    # =========================================
    # PLAYER RESULTS
    # =========================================
    players = game_result["players"]

    for p in players:

        profit = (
            p["stack"]
            - START_STACK
        )

        result = {

            "hand_id": hand_id,

            "player": p["name"],

            "stack": p["stack"],

            "profit": profit
        }

        all_results.append(result)

# =========================================
# FINAL SUMMARY
# =========================================
print(
    "\n========== FINAL SUMMARY ==========\n"
)

print(
    f"Target Hands : {TARGET_HANDS}"
)

print(
    f"Actual Hands : {total_hands_played}"
)

# =========================================
# FINAL BB/100
# =========================================
print(
    "\n========== FINAL RESULT ==========\n"
)

players_summary = {

    "GPTBot": gpt_player,

    "GeminiBot": gemini_player,

    "ClaudeBot": claude_player
}

for name, player_obj in players_summary.items():

    total_profit = (
        player_obj.cumulative_profit
    )

    total_bb = (
        total_profit / BIG_BLIND
    )

    bb_100 = (
        total_bb / TARGET_HANDS
    ) * 100

    print(
        f"{name} | "
        f"Profit: {total_profit} | "
        f"BB/100: {bb_100:.2f}"
    )

# =========================================
# SAVE CSV
# =========================================
df = pd.DataFrame(all_results)

csv_path = (
    f"logs/game_results_{timestamp}.csv"
)

df.to_csv(
    csv_path,
    index=False
)

print("\n✅ CSV SAVED")

print(csv_path)