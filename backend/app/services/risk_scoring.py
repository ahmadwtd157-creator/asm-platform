class RiskScoringService:
    HIGH_RISK_PORTS = {3306, 5432, 6379, 27017}
    MEDIUM_RISK_PORTS = {22, 21 , 25}
    LOW_RISK_PORTS = {80, 443}

    @staticmethod
    def calculate(open_ports):
        """
        open_ports: list of dicts
        [{"port":80, "service": "http"}, ...]
        """
        score = 0
        for port_data in open_ports:
            port = port_data["port"]

            if port in RiskScoringService.HIGH_RISK_PORTS:
                score += 40

            elif port in RiskScoringService.MEDIUM_RISK_PORTS:
                score +=20
            elif port in RiskScoringService.LOW_RISK_PORTS:
                score += 5
            else:
                score +=10
        return min(score,100)