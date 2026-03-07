class AssetClassifier:

    PORT_RULES = {
        22: ("SSH Server", "Infrastructure", "Medium"),
        80: ("Web Server", "Application", "Low"),
        443: ("Web Server", "Application", "Low"),
        21: ("FTP", "File Transfer", "High"),
        25: ("SMTP Server", "Email", "Medium"),
        3306: ("MySQL Database", "Database", "High"),
        5432: ("PostgreSQL Database", "Database", "High"),
        27017: ("MongoDB", "Database", "High"),
        6379: ("Redis","Cache","High"),
        9200: ("Elasticsearch","search Engine","High"),
        3389: ("RDP", "Remote Access", "High"),
    }

    BANNER_KEYWORDS = {
        "apache": ("Web Server", "Application", "Low"),
        "nginx": ("Web Server", "Application", "Low"),
        "iis": ("Web Server", "Application", "Low"),
        "openssh": ("SSH Server", "Infrastructure"),
        "mysql": ("Database", "Database", "High"),
        "postgres": ("Database","Database", "High"),
        "redis": ("Cache", "Cache", "High"),
        "Mongodb": ("Database", "Database", "High"),
        "elasticsearch": ("Search Engine", "Search Engine", "High"),

    }

    @classmethod
    def classify(cls, port: int,banner: str=""):
        if port in cls.PORT_RULES:
            return cls.PORT_RULES[port]

        banner_lower = (banner or "").lower()
        for keyword, value in cls.BANNER_KEYWORDS.items():
            if keyword in banner_lower:
                return value
        return("Unknown Service", "Uncategorized", "Low")
        


