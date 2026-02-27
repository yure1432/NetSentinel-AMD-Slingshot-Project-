import logging

import paramiko


class SSHBase:
    """Base class for SSH operations."""

    def __init__(self):
        self.user = "ubuntu"
        self.key_path = "/home/you/.ssh/id_rsa"

    def get_client(self, ip: str):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=self.user, key_filename=self.key_path)
        return client


class SystemCollector(SSHBase):

    def collect(self, ip: str) -> dict:
        try:
            with self.get_client(ip) as ssh:
                return {
                    "ip": ip,
                    "ssh_password_auth": "yes"
                    in self._run(
                        ssh,
                        "grep PasswordAuthentication /etc/ssh/sshd_config || echo no",
                    ),
                    "firewall_enabled": "Status: active"
                    in self._run(ssh, "ufw status"),
                    "outdated_packages": self._run(
                        ssh, "apt list --upgradable 2>/dev/null"
                    ),
                }
        except Exception as e:
            logging.error(f"Collection failed for {ip}: {e}")
            return {}

    def _run(self, ssh, cmd):
        _, stdout, _ = ssh.exec_command(cmd)
        return stdout.read().decode().strip()


class ActionExecutor(SSHBase):

    def __init__(self):
        super().__init__()
        self.action_map = {
            "secure_ssh": self.secure_ssh,
            "enable_firewall": self.enable_firewall,
            "patch_system": self.patch_system,
        }

    def apply(self, ip: str, action_key: str):
        if action_key in self.action_map:
            self.action_map[action_key](ip)

    def secure_ssh(self, ip: str):
        logging.info(f"[{ip}] Securing SSH...")
        self._exec(
            ip,
            "sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && sudo systemctl restart ssh",
        )

    def enable_firewall(self, ip: str):
        logging.info(f"[{ip}] Enabling Firewall...")
        self._exec(ip, "sudo ufw --force enable")

    def patch_system(self, ip: str):
        logging.info(f"[{ip}] Patching Packages...")
        self._exec(ip, "sudo apt update && sudo apt upgrade -y")

    def _exec(self, ip, cmd):
        with self.get_client(ip) as ssh:
            ssh.exec_command(cmd)
