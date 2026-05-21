import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================================
# LOAD DATA
# =========================================
CSV_PATH = "logs/hand_profit.csv"

if not os.path.exists(CSV_PATH):

    print("❌ hand_profit.csv not found")
    exit()

df = pd.read_csv(CSV_PATH)

# =========================================
# CHECK DATA
# =========================================
if df.empty:

    print("❌ CSV file is empty")
    exit()

print("\n========== DATA PREVIEW ==========\n")
print(df.head())

# =========================================
# CREATE OUTPUT FOLDER
# =========================================
os.makedirs("logs/graphs", exist_ok=True)

# =========================================
# CUMULATIVE WINNINGS GRAPH
# =========================================
players = df["player"].unique()

plt.figure(figsize=(12, 6))

for player in players:

    player_df = df[
        df["player"] == player
    ]

    plt.plot(

        range(len(player_df)),

        player_df["cumulative_profit"],

        label=player
    )

# =========================================
# GRAPH SETTINGS
# =========================================
plt.title(
    "Cumulative Winnings Graph"
)

plt.xlabel("Hands")

plt.ylabel("Cumulative Profit")

plt.legend()

plt.grid(True)

# =========================================
# SAVE GRAPH
# =========================================
graph_path = (
    "logs/graphs/cumulative_winnings.png"
)

plt.savefig(graph_path)

print("\n✅ Graph saved:")
print(graph_path)

# =========================================
# SHOW GRAPH
# =========================================
plt.show()

# =========================================
# BB/100 ANALYSIS
# =========================================
print("\n========== BB/100 ==========\n")

BIG_BLIND = 20

for player in players:

    player_df = df[
        df["player"] == player
    ]

    total_profit = (
        player_df["hand_profit"].sum()
    )

    total_hands = (
        player_df["hand_id"].nunique()
    )

    bb_100 = (
        (total_profit / BIG_BLIND)
        / (total_hands / 100)
    )

    print(
        f"{player} BB/100 = "
        f"{bb_100:.2f}"
    )

# =========================================
# VARIANCE ANALYSIS
# =========================================
print("\n========== VARIANCE ==========\n")

for player in players:

    player_df = df[
        df["player"] == player
    ]

    variance = (
        player_df["hand_profit"].std()
    )

    print(
        f"{player} Std Dev = "
        f"{variance:.2f}"
    )

# =========================================
# SAMPLE SIZE
# =========================================
print("\n========== SAMPLE SIZE ==========\n")

for player in players:

    player_df = df[
        df["player"] == player
    ]

    total_hands = (
        player_df["hand_id"].nunique()
    )

    print(
        f"{player}: "
        f"{total_hands} hands"
    )

# =========================================
# AVG PROFIT / HAND
# =========================================
print("\n========== AVG PROFIT / HAND ==========\n")

for player in players:

    player_df = df[
        df["player"] == player
    ]

    avg_profit = (
        player_df["hand_profit"].mean()
    )

    print(
        f"{player}: "
        f"{avg_profit:.2f}"
    )