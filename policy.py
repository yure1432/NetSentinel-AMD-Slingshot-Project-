SAFE_ACTIONS = [
    "secure_ssh",
    "disable_root_ssh",
    "enable_firewall",
    "enable_fw_logging",
    "patch_system",
    "remove_insecure_services",
    "fix_config_perms",
]


def filter_actions(recommendations):
    allowed = []
    for rec in recommendations:
        action = rec.get("action")
        if action in SAFE_ACTIONS:
            allowed.append(action)
    return allowed
