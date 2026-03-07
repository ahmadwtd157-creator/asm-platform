import subprocess
import xml.etree.ElementTree as ET


class PortScanService:

    @staticmethod
    def scan(ip: str):

        command = [
            "nmap",
            "-sS",                 # SYN scan
            "-sV",                 # service detection
            "-T4",                 # faster timing
            "--top-ports", "50",   # تقليل عدد المنافذ
            "--max-retries", "1",
            "--host-timeout", "60s",
            "-Pn",
            "-oX", "-",            # XML output
            ip
        ]

        try:

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=90
            )

            if result.returncode != 0:
                raise Exception(f"Nmap error: {result.stderr}")

            if not result.stdout:
                raise Exception("Empty scan result")

            return PortScanService.parse_nmap_xml(result.stdout)

        except subprocess.TimeoutExpired:
            raise Exception("Nmap scan timed out")

        except Exception as e:
            raise Exception(f"Port scan failed: {str(e)}")



    @staticmethod
    def parse_nmap_xml(xml_output: str):

        try:
            root = ET.fromstring(xml_output)

        except ET.ParseError:
            raise Exception("Invalid Nmap XML output")

        open_ports = []

        for host in root.findall("host"):

            ports = host.find("ports")

            if ports is None:
                continue

            for port in ports.findall("port"):

                state_elem = port.find("state")

                if state_elem is None:
                    continue

                state = state_elem.attrib.get("state")

                if state != "open":
                    continue

                port_id = int(port.attrib.get("portid"))

                service_elem = port.find("service")

                service_name = "unknown"
                banner = ""

                if service_elem is not None:

                    service_name = service_elem.attrib.get("name", "unknown")

                    product = service_elem.attrib.get("product", "")
                    version = service_elem.attrib.get("version", "")
                    extra = service_elem.attrib.get("extrainfo", "")

                    banner = " ".join(
                        part for part in [product, version, extra] if part
                    )

                open_ports.append({
                    "port": port_id,
                    "service": service_name,
                    "banner": banner,
                    "is_open": True
                })

        return open_ports