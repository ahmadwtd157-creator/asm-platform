import subprocess
import json

def run_subfinder(domain: str):
    command = [
        "subfinder",
        "-d",
        domain,
        "-silent",
        "-oJ"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    subdomains = []

    for line in result.stdout.splitlines():
        try:
            data = json.loads(line)
            host = data.get("host")
            if host:
                subdomains.append(host)
        except Exception:
            continue
    return list(set(subdomains))