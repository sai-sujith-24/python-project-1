from datetime import datetime
from urllib.parse import urlsplit
from ipaddress import ip_address
import re

from flask import Flask, render_template, request

app = Flask(__name__)

SUSPICIOUS_WORDS = {"login", "verify", "secure", "bank", "update", "free", "bonus", "gift"}


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/scan")
def scan():
    url = request.form.get("url", "").strip()
    if not url or len(url) > 2048:
        return "Enter a valid URL of at most 2048 characters.", 400
    try:
        parsed = urlsplit(url)
        if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
            raise ValueError("URL must use HTTP or HTTPS and have a hostname")
        host = parsed.hostname.lower()
        if any(ch.isspace() for ch in host):
            raise ValueError("Invalid hostname")
        # Accessing .port also validates invalid port values.
        _ = parsed.port
    except ValueError:
        return "Enter a valid HTTP or HTTPS website URL.", 400

    # These are simple indicators only; they do not establish whether a site is safe.
    indicators = []
    if len(url) > 80:
        indicators.append("Unusually long URL")
    if parsed.scheme.lower() != "https":
        indicators.append("HTTPS not used")
    if parsed.username is not None or parsed.password is not None:
        indicators.append("URL contains user-info before the hostname")
    try:
        ip_address(host)
        indicators.append("Hostname is an IP address")
    except ValueError:
        pass

    # Match keywords in the hostname only, to avoid flagging ordinary search queries.
    if any(re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", host) for word in SUSPICIOUS_WORDS):
        indicators.append("Risk-related hostname keywords")

    context = {
        "url": url,
        "scan_time": datetime.now().strftime("%b %d, %Y - %I:%M %p"),
        "indicators": indicators,
    }
    return render_template("phishing.html" if indicators else "safe.html", **context)


if __name__ == "__main__":
    # Use a local development server. Never deploy with Flask debug mode enabled.
    app.run(host="127.0.0.1", port=5000, debug=False)
