import streamlit as st
import requests
import json

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FraudGuard AI")
st.subheader("Agentic AI Fraud Investigation Dashboard")
st.caption("Streamlit UI connected to an n8n fraud-investigation workflow")

with st.sidebar:
    st.header("n8n Connection")
    webhook_url = st.text_input(
        "n8n Webhook URL",
        placeholder="Paste your n8n Test URL here"
    )
    st.info("For the first demo, use the n8n Test URL. Keep the workflow listening in n8n while testing.")

st.markdown("### Submit Fraud Alert")

col1, col2 = st.columns(2)

with col1:
    transaction_id = st.text_input("Transaction ID", "FRD-UI-001")
    customer_id = st.text_input("Customer ID", "CUST-1001")
    amount = st.number_input("Amount (INR)", min_value=1.0, value=1250.0, step=100.0)
    merchant = st.text_input("Merchant", "Amazon India")
    merchant_category = st.text_input("Merchant Category", "Retail")

with col2:
    device_id = st.text_input("Device ID", "DEV-1001")
    ip_address = st.text_input("IP Address", "103.25.10.20")
    country = st.text_input("Country", "India")
    currency = st.text_input("Currency", "INR")

payload = {
    "transaction_id": transaction_id,
    "customer_id": customer_id,
    "amount": amount,
    "currency": currency,
    "merchant": merchant,
    "merchant_category": merchant_category,
    "device_id": device_id,
    "ip_address": ip_address,
    "country": country,
}

st.markdown("### Test Cases")
t1, t2, t3 = st.columns(3)

with t1:
    if st.button("🟢 Load Normal Case"):
        st.session_state["case"] = {
            "transaction_id": "FRD-LOW-001",
            "customer_id": "CUST-1001",
            "amount": 1250,
            "currency": "INR",
            "merchant": "Amazon India",
            "merchant_category": "Retail",
            "device_id": "DEV-1001",
            "ip_address": "103.25.10.20",
            "country": "India",
        }
        st.rerun()

with t2:
    if st.button("🟡 Load Ambiguous Case"):
        st.session_state["case"] = {
            "transaction_id": "FRD-AMB-001",
            "customer_id": "CUST-1001",
            "amount": 48000,
            "currency": "INR",
            "merchant": "Unknown Online Merchant",
            "merchant_category": "Electronics",
            "device_id": "DEV-NEW-100",
            "ip_address": "192.168.1.50",
            "country": "India",
        }
        st.rerun()

with t3:
    if st.button("🔴 Load High-Risk Case"):
        st.session_state["case"] = {
            "transaction_id": "FRD-HIGH-001",
            "customer_id": "CUST-HIGH-001",
            "amount": 250000,
            "currency": "INR",
            "merchant": "Unknown International Merchant",
            "merchant_category": "Gambling",
            "device_id": "DEV-NEW-999",
            "ip_address": "10.0.0.55",
            "country": "India",
        }
        st.rerun()

if "case" in st.session_state:
    c = st.session_state["case"]
    st.info(f"Loaded: {c['transaction_id']}")
    st.json(c)

st.divider()

if st.button("🚀 Investigate Transaction", type="primary"):
    if not webhook_url:
        st.error("Paste your n8n Webhook URL in the sidebar first.")
    else:
        try:
            with st.spinner("Sending fraud alert to n8n..."):
                response = requests.post(
                    webhook_url,
                    json=payload,
                    timeout=120
                )

            st.write(f"n8n HTTP status: **{response.status_code}**")

            try:
                result = response.json()
                st.success("Fraud alert reached n8n.")
                st.subheader("Investigation Result")
                st.json(result)
            except ValueError:
                st.success("Fraud alert reached n8n.")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to n8n: {e}")

st.divider()
st.caption("FraudGuard AI — Stage 3 Agentic Fraud Investigation PoC")
