import logging

import paramiko


class SSHBase:
    """Base class for SSH operations."""

    def __init__(self):
        # Update these for your Arch user and target environment
        self.user = "ubuntu"
        self.key_path = "/home/you/.ssh/id_rsa"

    def get_client(self, ip: str):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=self.user, key_filename=self.key_path)
        return client


class ActionExecutor(SSHBase):
    """Executes security remediation based on AI analysis."""

    def __init__(self):
        super().__init__()
        self.action_map = {
            "secure_ssh": self.secure_ssh,
            "enable_firewall": self.enable_firewall,
            "patch_system": self.patch_system,
            "disable_root_ssh": self.disable_root_ssh,
            "remove_insecure_services": self.remove_insecure_services,
            "fix_config_perms": self.fix_config_perms,
            "enable_fw_logging": self.enable_fw_logging,
        }

    def apply(self, ip: str, action_key: str):
        if action_key in self.action_map:
            self.action_map[action_key](ip)

    def _exec(self, ip, cmd):
        """Helper to run sudo commands."""
        with self.get_client(ip) as ssh:
            ssh.exec_command(cmd)

    def secure_ssh(self, ip: str):
        logging.info(f"[{ip}] Disabling Password Auth...")
        self._exec(
            ip,
            "sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && sudo systemctl restart ssh",
        )

    def disable_root_ssh(self, ip: str):
        logging.info(f"[{ip}] Disabling Root SSH Login...")
        self._exec(
            ip,
            "sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && sudo systemctl restart ssh",
        )

    def enable_firewall(self, ip: str):
        logging.info(f"[{ip}] Enabling UFW...")
        self._exec(ip, "sudo ufw --force enable")

    def enable_fw_logging(self, ip: str):
        logging.info(f"[{ip}] Enabling UFW Logging...")
        self._exec(ip, "sudo ufw logging on")

    def patch_system(self, ip: str):
        logging.info(f"[{ip}] Running Updates...")
        self._exec(ip, "sudo apt update && sudo apt upgrade -y")

    def remove_insecure_services(self, ip: str):
        logging.info(f"[{ip}] Purging Insecure Services...")
        self._exec(
            ip,
            "sudo apt purge -y telnetd ftpd rsh-server ypbind && sudo systemctl daemon-reload",
        )

    def fix_config_perms(self, ip: str):
        logging.info(f"[{ip}] Hardening File Permissions...")
        self._exec(
            ip, "sudo find /etc -maxdepth 2 -perm -0002 -type f -exec chmod o-w {} +"
        )
