from urllib.parse import urlsplit


def extract_features(url):
    """Seven lexical features used by the optional training experiment."""
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    suspicious = ("login", "verify", "bank", "secure")
    return [
        len(url),
        int(parsed.scheme.lower() == "https"),
        host.count("."),
        url.count("-"),
        url.count("@"),
        sum(c.isdigit() for c in url),
        sum(word in host.lower() for word in suspicious),
    ]
