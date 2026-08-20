from urllib.parse import urlparse

def extract_features(url):
    features = []

    # URL Length
    features.append(len(url))

    # HTTPS check
    features.append(1 if "https" in url else 0)

    # Count dots
    features.append(url.count('.'))

    # Count hyphens
    features.append(url.count('-'))

    # Count @ symbols
    features.append(url.count('@'))

    # Count digits
    features.append(sum(c.isdigit() for c in url))

    # Suspicious words
    suspicious_words = ['login', 'verify', 'bank', 'secure']

    features.append(
        sum(word in url.lower() for word in suspicious_words)
    )

    return features