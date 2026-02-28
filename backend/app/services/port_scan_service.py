import subprocess
import xml.etree.ElementTree as ET

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
            text=True,
            timeout=300
        )

        return PortScanService.parse_nmap_xml(result.stdout)

    @staticmethod
    def parse_nmap_xml(xml_output: str):
        root = ET.fromstring(xml_output)

        open_ports =[]

        for host in root.findall("host"):
            for port in host.findall(".//port"):
                state = port.find("state")

                if state is not None and state.attrib.get("state") == "open":
                    port_id = int(port.attrib.get("portid"))
                    service_elem = port.find("service")

                    service_name = ""
                    banner = ""

                    if service_elem is not None:
                        service_name = service_elem.attrib.get("name","")
                        product = service_elem.attrib.get("product","")
                        version =  service_elem.attrib.get("version","")      
                        banner = f"{product} {version}".strip()

                    open_ports.append({
                        "port": port_id,
                        "service": service_name,
                        "banner": banner

                    })

        return open_ports
        