def rule_based_decision(valid_actions, hole_card, round_state):
    """
    return:
    {
        "action": "fold|call|raise",
        "amount": number,
        "confidence": 0.0 - 1.0
    }
    """

    street = round_state.get("street", "")
    ranks = [c[1] for c in hole_card]

    # หา call amount
    call_amount = 0
    raise_min = None
    for a in valid_actions:
        if a["action"] == "call":
            call_amount = a["amount"]
        if a["action"] == "raise":
            raise_min = a["amount"]["min"]

    # ===== PRE-FLOP =====
    if street == "preflop":
        # ไพ่ใหญ่
        if "A" in ranks or "K" in ranks:
            if raise_min:
                return {
                    "action": "raise",
                    "amount": raise_min,
                    "confidence": 0.8
                }
            else:
                return {
                    "action": "call",
                    "amount": call_amount,
                    "confidence": 0.7
                }

        # ไพ่กลาง
        if ranks[0] == ranks[1]:
            return {
                "action": "call",
                "amount": call_amount,
                "confidence": 0.6
            }

        # ไพ่กาก
        return {
            "action": "fold",
            "amount": 0,
            "confidence": 0.9
        }

    # ===== POST-FLOP =====
    if street in ["flop", "turn", "river"]:
        # default conservative
        if call_amount == 0:
            return {
                "action": "call",
                "amount": 0,
                "confidence": 0.4
            }

        if call_amount <= 10:
            return {
                "action": "call",
                "amount": call_amount,
                "confidence": 0.5
            }

        return {
            "action": "fold",
            "amount": 0,
            "confidence": 0.7
        }

