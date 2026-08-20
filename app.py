from flask import Flask, render_template, request
from datetime import datetime
import re

app = Flask(__name__)


# HOME PAGE

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# URL SCAN

@app.route("/scan", methods=["POST"])
def scan():

    url = request.form["url"].strip()

    suspicious_words = [

        "login",
        "verify",
        "secure",
        "bank",
        "update",
        "free",
        "bonus",
        "gift",
        "xyz",
        "ru"

    ]

    phishing = False


    # LONG URL

    if len(url) > 80:

        phishing = True


    # HTTP / HTTPS

    if not (

        url.startswith("http://")
        or
        url.startswith("https://")

    ):

        phishing = True


    # @ SYMBOL

    if "@" in url:

        phishing = True


    # IP ADDRESS

    if re.search(

        r"\d+\.\d+\.\d+\.\d+",

        url

    ):

        phishing = True


    # KEYWORDS

    for word in suspicious_words:

        if word in url.lower():

            phishing = True

            break


    # SYSTEM TIME

    current_time = datetime.now().strftime(

        "%b %d, %Y • %I:%M %p"

    )


    # RESULT

    if phishing:

        return render_template(

            "phishing.html",

            url=url,

            scan_time=current_time

        )


    return render_template(

        "safe.html",

        url=url,

        scan_time=current_time

    )


# RUN SERVER

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )