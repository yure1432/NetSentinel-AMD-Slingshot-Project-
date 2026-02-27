import paramiko

USER = "ubuntu"
KEY = "/home/you/.ssh/id_rsa"


def run_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode().strip()


def collect_state(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=USER, key_filename=KEY)

    state = {
        "ip": ip,
        "ssh_password_auth": "yes"
        in run_cmd(ssh, "grep PasswordAuthentication /etc/ssh/sshd_config || echo no"),
        "firewall_enabled": "Status: active" in run_cmd(ssh, "ufw status"),
        "outdated_packages": run_cmd(ssh, "apt list --upgradable 2>/dev/null"),
    }

    ssh.close()
    return state
