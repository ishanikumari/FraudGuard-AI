# FraudGuard AI — Streamlit UI

This is the Stage 3 user interface for the FraudGuard AI n8n workflow.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then paste the n8n Transaction Webhook Test URL into the sidebar.

## Important

The n8n workflow must be listening for the Test URL while you click "Investigate Transaction".
