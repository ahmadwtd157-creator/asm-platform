import subprocess
import json

def run_subfinder(domain):
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
        text=True
    )
    
    subdomains = []

    for line in result.stdout.splitlines():
        try:
            data = josn.loads(line)
            subdomains.append(data.get("host"))
        except Exception:
            continue
    return list(set(subdomains))