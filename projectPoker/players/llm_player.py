# players/llm_player.py

from pypokerengine.players import BasePokerPlayer

import json
import os
import time

from datetime import datetime

from utils.save_csv import add_log

LOG_PATH = "logs/actions.jsonl"

# =========================================
# SAVE LOG FILE
# =========================================
def log_action(data):

    os.makedirs("logs", exist_ok=True)

    # =========================================
    # JSON LOG
    # =========================================
    with open(
        LOG_PATH,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                data,
                ensure_ascii=False
            ) + "\n"
        )

    # =========================================
    # READABLE LOG
    # =========================================
    with open(
        "logs/readable_log.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(f"""
========================================
Time    : {data['time']}

Game ID : {data['game_id']}

Player  : {data['player']}

Hand ID : {data.get('hand_id')}

Street  : {data['street']}

Cards   : {data['hole_card']}

Board   : {data['community_card']}

Pot     : {data['pot_size']}

Stack   : {data['stack']}

Action  : {data['final_action']}

Amount  : {data['final_amount']}

Raise   : {data.get('is_raise')}

Call    : {data.get('is_call')}

Fold    : {data.get('is_fold')}
========================================
""")

# =========================================
# LLM PLAYER
# =========================================
class LLMPlayer(BasePokerPlayer):

    def __init__(
        self,
        advisor,
        name,
        game_id
    ):

        self.advisor = advisor

        self.name = name

        self.game_id = game_id

        # =========================================
        # RESEARCH METRICS
        # =========================================
        self.initial_stack = None

        self.round_start_stack = 0

        self.cumulative_profit = 0

        # =========================================
        # GLOBAL HAND TRACKER
        # =========================================
        self.global_hand_id = 0

    # =========================================
    # GAME START
    # =========================================
    def receive_game_start_message(
        self,
        game_info
    ):
        pass

    # =========================================
    # ROUND START
    # =========================================
    def receive_round_start_message(
        self,
        round_count,
        hole_card,
        seats
    ):

        me = next(
            p for p in seats
            if p["uuid"] == self.uuid
        )

        self.round_start_stack = me["stack"]

        if self.initial_stack is None:

            self.initial_stack = me["stack"]

        # =========================================
        # GLOBAL HAND COUNTER
        # =========================================
        self.global_hand_id += 1

    # =========================================
    # STREET START
    # =========================================
    def receive_street_start_message(
        self,
        street,
        round_state
    ):
        pass

    # =========================================
    # GAME UPDATE
    # =========================================
    def receive_game_update_message(
        self,
        action,
        round_state
    ):
        pass

    # =========================================
    # ROUND RESULT
    # =========================================
    def receive_round_result_message(
        self,
        winners,
        hand_info,
        round_state
    ):

        me = next(
            p for p in round_state["seats"]
            if p["uuid"] == self.uuid
        )

        current_stack = me["stack"]

        # =========================================
        # HAND PROFIT
        # =========================================
        hand_profit = (
            current_stack
            - self.round_start_stack
        )

        # =========================================
        # CUMULATIVE PROFIT
        # =========================================
        self.cumulative_profit += hand_profit

        # =========================================
        # BB PROFIT
        # =========================================
        BIG_BLIND = 20

        bb_profit = (
            hand_profit / BIG_BLIND
        )

        # =========================================
        # SAVE HAND PROFIT
        # =========================================
        with open(
            "logs/hand_profit.csv",
            "a",
            encoding="utf-8"
        ) as f:

            if f.tell() == 0:

                f.write(
                    "game_id,"
                    "hand_id,"
                    "player,"
                    "stack,"
                    "hand_profit,"
                    "bb_profit,"
                    "cumulative_profit\n"
                )

            f.write(
                f"{self.game_id},"
                f"{self.global_hand_id},"
                f"{self.name},"
                f"{current_stack},"
                f"{hand_profit},"
                f"{bb_profit},"
                f"{self.cumulative_profit}\n"
            )

        # =========================================
        # PRINT RESULT
        # =========================================
        if self.name == "GPTBot":

            winner_names = [
                w["name"]
                for w in winners
            ]

            print(
                f"\n🏆 HAND WINNER: "
                f"{winner_names}"
            )

            print(
                f"📈 GPTBot "
                f"Cumulative Profit: "
                f"{self.cumulative_profit}"
            )

    # =========================================
    # CORE DECISION ENGINE
    # =========================================
    def declare_action(
        self,
        valid_actions,
        hole_card,
        round_state
    ):

        call_amount = 0

        valid_action_names = []

        for a in valid_actions:

            valid_action_names.append(
                a["action"]
            )

            if a["action"] == "call":

                call_amount = a["amount"]

        try:

            my_uuid = self.uuid

            players = round_state["seats"]

            # =========================================
            # STACK
            # =========================================
            my_stack = next(
                p["stack"]
                for p in players
                if p["uuid"] == my_uuid
            )

            # =========================================
            # POSITION
            # =========================================
            position = next(
                (
                    i for i, p
                    in enumerate(players)
                    if p["uuid"] == my_uuid
                ),
                -1
            )

            # =========================================
            # AI DECISION WITH RETRY
            # =========================================
            advice = None

            for attempt in range(3):

                try:

                    advice = self.advisor.analyze(
                        round_state,
                        hole_card,
                        position,
                        valid_actions
                    )

                    break

                except Exception as e:

                    print(
                        f"AI error "
                        f"(attempt {attempt + 1}/3):",
                        e
                    )

                    # =========================================
                    # WAIT BEFORE RETRY
                    # =========================================
                    time.sleep(5)

            # =========================================
            # FINAL FALLBACK
            # =========================================
            if advice is None:

                return "call", call_amount

        except Exception as e:

            print("Critical error:", e)

            return "call", call_amount

        # =========================================
        # SAFE FALLBACK
        # =========================================
        if not isinstance(advice, dict):

            action = "call"

            amount = call_amount

        else:

            action = advice.get(
                "action",
                "call"
            )

            amount = advice.get(
                "amount",
                call_amount
            )

        # =========================================
        # PREVENT OVER STACK BET
        # =========================================
        amount = min(
            amount,
            my_stack
        )

        # =========================================
        # VALID ACTION CHECK
        # =========================================
        if action not in valid_action_names:

            action = "call"

            amount = call_amount

        # =========================================
        # STACK + POT
        # =========================================
        pot_size = (
            round_state["pot"]
            ["main"]
            ["amount"]
        )

        # =========================================
        # RESEARCH FEATURES
        # =========================================
        hand_id = self.global_hand_id

        is_raise = action == "raise"

        is_call = action == "call"

        is_fold = action == "fold"

        # =========================================
        # LOG ACTION
        # =========================================
        log_action({

            "time": datetime.now().isoformat(),

            "game_id": self.game_id,

            "player": self.name,

            "hand_id": hand_id,

            "street": round_state.get(
                "street",
                ""
            ),

            "hole_card": hole_card,

            "final_action": action,

            "final_amount": amount,

            "community_card": round_state.get(
                "community_card",
                []
            ),

            "stack": my_stack,

            "pot_size": pot_size,

            "is_raise": is_raise,

            "is_call": is_call,

            "is_fold": is_fold
        })

        # =========================================
        # CSV LOG
        # =========================================
        add_log(

            game_id=self.game_id,

            round_id=hand_id,

            player=self.name,

            street=round_state["street"],

            hand_cards=hole_card,

            action=action,

            amount=amount,

            board_cards=round_state[
                "community_card"
            ],

            stack_before=my_stack,

            pot_size=pot_size,

            position=f"seat_{position}",

            is_raise=is_raise,

            is_call=is_call,

            is_fold=is_fold,

            timestamp=datetime.now().isoformat()
        )

        # =========================================
        # TERMINAL OUTPUT
        # =========================================
        print(
            f"""
========================================
Game    : {self.game_id}

Hand    : {hand_id}

Street  : {round_state.get('street')}

Player  : {self.name}

Cards   : {hole_card}

Board   : {round_state.get('community_card', [])}

Pot     : {pot_size}

Stack   : {my_stack}

Action  : {action}

Amount  : {amount}
========================================
"""
        )

        # =========================================
        # RATE LIMIT PROTECTION
        # =========================================
        time.sleep(1)

        return action, amount