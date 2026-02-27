SAFE_ACTIONS = ["secure_ssh", "enable_firewall", "patch_system"]


def filter_actions(actions):
    allowed = []
    for a in actions:
        if a["action"] in SAFE_ACTIONS:
            allowed.append(a["action"])
    return allowed
