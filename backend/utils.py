import re
from urllib.parse import urlparse

def extract_lexical_features(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    
    # 1. IP address check in domain
    ip_pattern = re.compile(
        r"^(?:http[s]?://)?(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
    )
    has_ip = bool(ip_pattern.match(url))
    
    # 2. Suspicious keywords often used in phishing
    suspicious_keywords = ["login", "verify", "secure", "update", "bank", "account", "signin", "confirm"]
    found_keywords = [kw for kw in suspicious_keywords if kw in url.lower()]
    
    features = {
        "url_length": len(url),
        "domain_length": len(domain),
        "has_ip_address": has_ip,
        "subdomain_count": domain.count('.') - 1 if domain else 0,
        "special_char_count": url.count('@') + url.count('-') + url.count('_'),
        "suspicious_keywords": found_keywords,
        "https_used": parsed.scheme == "https"
    }
    return features