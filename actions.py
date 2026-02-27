import paramiko

USER = "ubuntu"
KEY = "/home/you/.ssh/id_rsa"


def ssh_exec(ip, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=USER, key_filename=KEY)
    ssh.exec_command(cmd)
    ssh.close()


def secure_ssh(ip):
    print(f"[{ip}] Securing SSH")
    ssh_exec(
        ip,
        "sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config",
    )
    ssh_exec(ip, "sudo systemctl restart ssh")


def enable_firewall(ip):
    print(f"[{ip}] Enabling firewall")
    ssh_exec(ip, "sudo ufw --force enable")


def patch_system(ip):
    print(f"[{ip}] Updating packages")
    ssh_exec(ip, "sudo apt update && sudo apt upgrade -y")


ACTION_MAP = {
    "secure_ssh": secure_ssh,
    "enable_firewall": enable_firewall,
    "patch_system": patch_system,
}
