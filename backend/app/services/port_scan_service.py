import subprocess
import json

class PortScanService:

    @staticmethod
    def scan(ip: str):
        command = [
            "nmap",
            "-sV",
            "-Pn",
            "--top-ports", "1000",
            "-oX", "-",
            ip

        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return result.stdout
        