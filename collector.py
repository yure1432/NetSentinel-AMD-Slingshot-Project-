import logging

from actions import SSHBase


class SystemCollector(SSHBase):
    def collect(self, ip: str) -> dict:
        try:
            with self.get_client(ip) as ssh:
                return {
                    "ip": ip,
                    "ssh_password_auth": "yes"
                    in self._run(
                        ssh,
                        "grep '^PasswordAuthentication yes' /etc/ssh/sshd_config || echo no",
                    ),
                    "ssh_root_login": "yes"
                    in self._run(
                        ssh,
                        "grep '^PermitRootLogin yes' /etc/ssh/sshd_config || echo no",
                    ),
                    "firewall_enabled": "Status: active"
                    in self._run(ssh, "sudo ufw status"),
                    "firewall_logging": "Logging: on"
                    in self._run(ssh, "sudo ufw status verbose | grep Logging"),
                    "outdated_packages": self._run(
                        ssh, "apt list --upgradable 2>/dev/null"
                    ),
                    "empty_password_accounts": self._run(
                        ssh, "sudo awk -F: '($2 == \"\") {print $1}' /etc/shadow"
                    ),
                    "insecure_services_active": self._run(
                        ssh,
                        "systemctl is-active telnet ftp rsh 2>/dev/null || echo none",
                    ),
                    "world_writable_configs": self._run(
                        ssh, "find /etc -maxdepth 2 -perm -0002 -type f 2>/dev/null"
                    ),
                    "listening_services": self._run(
                        ssh, "sudo ss -tulpn | grep LISTEN"
                    ),
                }
        except Exception as e:
            logging.error(f"Collection failed for {ip}: {e}")
            return {}

    def _run(self, ssh, cmd):
        _, stdout, _ = ssh.exec_command(cmd)
        return stdout.read().decode().strip()
