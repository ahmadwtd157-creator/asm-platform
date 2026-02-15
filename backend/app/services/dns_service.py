import subprocess
import json
from typing import List, Dict


class DNSService:

    @staticmethod
    def validate_subdomains(subdomains: List[str]) -> List[Dict]:
        """
        Validate subdomins using dnsx
        Returns structured DNS data
        """

        if not subdomains:
            return
        process = subprocess.run(
            [
                "dnsx",
                "-silent",
                "-a",
                "-aaaa",
                "-cname",
                "-rate-limit", "100",
                "-retrise", "2",
                "-json"
                

            
            ]
        )