# Phishing URL Risk Checker (Python / Flask)

An educational phishing-URL checker using transparent URL heuristics. **A low-risk result does not guarantee a website is safe.** The included `phishing_model.pkl` is an older demonstration artifact and is **not used** by the web application because its training data were too small to validate real-world accuracy.

## Run locally

```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. The Flask HTML pages are in `templates/`.

## How it works
The app validates HTTP/HTTPS URL structure and flags long URLs, plaintext HTTP, URL credentials, IP hostnames and some suspicious hostname keywords. Results are indicators, not guarantees. The tool does not visit or execute URLs.

## Optional machine-learning experiment

Provide a labeled CSV with columns `url,label` where `1` means phishing and `0` means benign. Then run:

```bash
python train_model.py your_labeled_dataset.csv --output phishing_model.pkl
```

The script prints holdout evaluation metrics. Use larger independently sourced datasets and proper validation before integrating a model into the live app.

## Next steps
Add tests covering normal URLs, misleading subdomains, invalid inputs, and known false positives. Do not deploy the Flask development server on the public internet.
