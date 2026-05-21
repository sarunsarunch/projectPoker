import csv
import os

CSV_PATH = "logs/poker_log.csv"

# =========================================
# CREATE CSV FILE
# =========================================
def create_csv():

    os.makedirs("logs", exist_ok=True)

    if not os.path.exists(CSV_PATH):

        with open(
            CSV_PATH,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                # =========================================
                # GAME INFO
                # =========================================
                "game_id",

                "round_id",

                "player",

                # =========================================
                # POKER STATE
                # =========================================
                "street",

                "hand_cards",

                "board_cards",

                # =========================================
                # ACTION
                # =========================================
                "action",

                "amount",

                # =========================================
                # STACK + POT
                # =========================================
                "stack_before",

                "pot_size",

                # =========================================
                # POSITION
                # =========================================
                "position",

                # =========================================
                # RESEARCH METRICS
                # =========================================
                "is_raise",

                "is_call",

                "is_fold",

                # =========================================
                # TIMESTAMP
                # =========================================
                "timestamp"
            ])

# =========================================
# ADD LOG
# =========================================
def add_log(

    game_id,

    round_id,

    player,

    street,

    hand_cards,

    action,

    amount,

    board_cards,

    stack_before,

    pot_size,

    position,

    is_raise,

    is_call,

    is_fold,

    timestamp
):

    create_csv()

    with open(
        CSV_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([

            # =========================================
            # GAME INFO
            # =========================================
            game_id,

            round_id,

            player,

            # =========================================
            # POKER STATE
            # =========================================
            street,

            hand_cards,

            board_cards,

            # =========================================
            # ACTION
            # =========================================
            action,

            amount,

            # =========================================
            # STACK + POT
            # =========================================
            stack_before,

            pot_size,

            # =========================================
            # POSITION
            # =========================================
            position,

            # =========================================
            # RESEARCH METRICS
            # =========================================
            is_raise,

            is_call,

            is_fold,

            # =========================================
            # TIMESTAMP
            # =========================================
            timestamp
        ])