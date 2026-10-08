import requests
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# BASIC STYLING
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# N8N PRODUCTION WEBHOOK
# =========================================================
# IMPORTANT:
# Do NOT put the actual webhook URL directly in this file.
#
# Add this in:
# Streamlit Cloud
# → App
# → Settings
# → Secrets
#
# N8N_WEBHOOK_URL = "your-production-webhook-url"
# =========================================================

try:
    N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]
except Exception:
    N8N_WEBHOOK_URL = ""


# =========================================================
# DEMO TEST CASES
# =========================================================

TEST_CASES = {

    "Normal — FRD-LOW-001": {

        "transaction_id": "FRD-LOW-001",

        "customer_id": "CUST-1001",

        "amount": 1250,

        "currency": "INR",

        "merchant": "Amazon India",

        "merchant_category": "Retail",

        "device_id": "DEV-1001",

        "ip_address": "103.25.10.20",

        "country": "India"
    },


    "Ambiguous — FRD-AMB-001": {

        "transaction_id": "FRD-AMB-001",

        "customer_id": "CUST-1001",

        "amount": 48000,

        "currency": "INR",

        "merchant": "Unknown Online Merchant",

        "merchant_category": "Electronics",

        "device_id": "DEV-NEW-100",

        "ip_address": "192.168.1.50",

        "country": "India"
    },


    "High Risk — FRD-HIGH-001": {

        "transaction_id": "FRD-HIGH-001",

        "customer_id": "CUST-HIGH-001",

        "amount": 250000,

        "currency": "INR",

        "merchant": "Unknown International Merchant",

        "merchant_category": "Gambling",

        "device_id": "DEV-NEW-999",

        "ip_address": "10.0.0.55",

        "country": "India"
    }
}


# =========================================================
# SESSION STATE
# =========================================================

if "case" not in st.session_state:

    st.session_state.case = (
        TEST_CASES["Normal — FRD-LOW-001"].copy()
    )


if "last_result" not in st.session_state:

    st.session_state.last_result = None


# =========================================================
# LOAD TEST CASE FUNCTION
# =========================================================

def load_case(case_name):

    st.session_state.case = TEST_CASES[case_name].copy()

    st.session_state.last_result = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🛡️ FraudGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Agentic AI-powered Fraud Investigation and Risk Assessment'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CONNECTION STATUS
# =========================================================

if N8N_WEBHOOK_URL:

    st.success(
        "Connected to configured n8n production webhook."
    )

else:

    st.error(
        "n8n webhook is not configured. "
        "Add N8N_WEBHOOK_URL in "
        "Streamlit Cloud → Settings → Secrets."
    )


# =========================================================
# DEMO TEST CASE BUTTONS
# =========================================================

st.subheader("Load Demo Test Case")


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "Load Normal Case",
        use_container_width=True
    ):

        load_case(
            "Normal — FRD-LOW-001"
        )

        st.rerun()


with col2:

    if st.button(
        "Load Ambiguous Case",
        use_container_width=True
    ):

        load_case(
            "Ambiguous — FRD-AMB-001"
        )

        st.rerun()


with col3:

    if st.button(
        "Load High-Risk Case",
        use_container_width=True
    ):

        load_case(
            "High Risk — FRD-HIGH-001"
        )

        st.rerun()


# =========================================================
# CURRENT CASE
# =========================================================

case = st.session_state.case


st.info(
    f"Currently loaded case: "
    f"**{case['transaction_id']}**"
)


# =========================================================
# TRANSACTION INPUT FORM
# =========================================================

st.subheader("Transaction Details")


with st.form("fraud_investigation_form"):

    left, right = st.columns(2)


    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

    with left:

        transaction_id = st.text_input(
            "Transaction ID",
            value=str(
                case["transaction_id"]
            )
        )


        customer_id = st.text_input(
            "Customer ID",
            value=str(
                case["customer_id"]
            )
        )


        amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=float(
                case["amount"]
            ),
            step=100.0
        )


        currency = st.text_input(
            "Currency",
            value=str(
                case["currency"]
            )
        )


        merchant = st.text_input(
            "Merchant",
            value=str(
                case["merchant"]
            )
        )


    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

    with right:

        merchant_category = st.text_input(
            "Merchant Category",
            value=str(
                case["merchant_category"]
            )
        )


        device_id = st.text_input(
            "Device ID",
            value=str(
                case["device_id"]
            )
        )


        ip_address = st.text_input(
            "IP Address",
            value=str(
                case["ip_address"]
            )
        )


        country = st.text_input(
            "Country",
            value=str(
                case["country"]
            )
        )


    submitted = st.form_submit_button(
        "🔍 Investigate Transaction",
        use_container_width=True
    )


# =========================================================
# SUBMIT TRANSACTION TO N8N
# =========================================================

if submitted:


    # -----------------------------------------------------
    # Check webhook configuration
    # -----------------------------------------------------

    if not N8N_WEBHOOK_URL:

        st.error(
            "Cannot submit the investigation because "
            "N8N_WEBHOOK_URL is not configured."
        )

        st.stop()


    # -----------------------------------------------------
    # Build payload
    # -----------------------------------------------------

    payload = {

        "transaction_id":
            transaction_id.strip(),

        "customer_id":
            customer_id.strip(),

        "amount":
            amount,

        "currency":
            currency.strip(),

        "merchant":
            merchant.strip(),

        "merchant_category":
            merchant_category.strip(),

        "device_id":
            device_id.strip(),

        "ip_address":
            ip_address.strip(),

        "country":
            country.strip()
    }


    # -----------------------------------------------------
    # Validate required fields
    # -----------------------------------------------------

    required_fields = [

        "transaction_id",

        "customer_id",

        "currency",

        "merchant",

        "merchant_category",

        "device_id",

        "ip_address",

        "country"
    ]


    missing_fields = [

        field

        for field in required_fields

        if not payload[field]
    ]


    if missing_fields:

        st.error(
            "Please complete the following fields: "
            + ", ".join(missing_fields)
        )

        st.stop()


    if payload["amount"] <= 0:

        st.error(
            "Amount must be greater than 0."
        )

        st.stop()


    # -----------------------------------------------------
    # Send to n8n
    # -----------------------------------------------------

    with st.spinner(
        "FraudGuard AI is investigating the transaction..."
    ):

        try:

            response = requests.post(

                N8N_WEBHOOK_URL,

                json=payload,

                timeout=120
            )


            response.raise_for_status()


            # -------------------------------------------------
            # Parse JSON response
            # -------------------------------------------------

            try:

                st.session_state.last_result = (
                    response.json()
                )

            except ValueError:

                st.session_state.last_result = {

                    "raw_response":
                        response.text
                }


        except requests.exceptions.Timeout:

            st.error(
                "The n8n workflow did not respond "
                "within 120 seconds."
            )

            st.info(
                "If this was a high-risk case, "
                "the workflow may be waiting for "
                "human approval through Gmail HITL."
            )


        except requests.exceptions.RequestException as exc:

            st.error(
                f"Unable to connect to the n8n workflow: {exc}"
            )


# =========================================================
# DISPLAY RESULT
# =========================================================

result = st.session_state.last_result


if result is not None:

    st.divider()

    st.subheader(
        "Investigation Result"
    )


    # -----------------------------------------------------
    # n8n sometimes returns a list
    # -----------------------------------------------------

    if isinstance(result, list) and result:

        result = result[0]


    # -----------------------------------------------------
    # Expected dictionary response
    # -----------------------------------------------------

    if isinstance(result, dict):


        output = result


        # ---------------------------------------------
        # Handle n8n "output"
        # ---------------------------------------------

        if isinstance(
            result.get("output"),
            dict
        ):

            output = result["output"]


        # ---------------------------------------------
        # Handle n8n "data"
        # ---------------------------------------------

        elif isinstance(
            result.get("data"),
            dict
        ):

            output = result["data"]


        # ---------------------------------------------
        # Nested output
        # ---------------------------------------------

        if isinstance(
            output.get("output"),
            dict
        ):

            output = output["output"]


        # ---------------------------------------------
        # Extract investigation fields
        # ---------------------------------------------

        risk_score = output.get(
            "risk_score"
        )


        risk_level = output.get(
            "risk_level"
        )


        verdict = output.get(
            "verdict"
        )


        explanation = output.get(
            "explanation"
        )


        red_flags = output.get(
            "red_flags",
            []
        )


        # ---------------------------------------------
        # Metrics
        # ---------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Risk Score",
                (
                    risk_score
                    if risk_score is not None
                    else "N/A"
                )
            )


        with col2:

            st.metric(
                "Risk Level",
                (
                    str(risk_level).upper()
                    if risk_level
                    else "N/A"
                )
            )


        with col3:

            st.metric(
                "Verdict",
                (
                    str(verdict).upper()
                    if verdict
                    else "N/A"
                )
            )


        # ---------------------------------------------
        # Explanation
        # ---------------------------------------------

        if explanation:

            st.markdown(
                "### Explanation"
            )

            st.write(
                explanation
            )


        # ---------------------------------------------
        # Red Flags
        # ---------------------------------------------

        if red_flags:

            st.markdown(
                "### Red Flags"
            )


            if isinstance(
                red_flags,
                list
            ):

                for flag in red_flags:

                    st.warning(
                        str(flag)
                    )

            else:

                st.warning(
                    str(red_flags)
                )


        # ---------------------------------------------
        # Human-in-the-Loop Decision
        # ---------------------------------------------

        human_decision = (

            result.get(
                "human_decision"
            )

            or output.get(
                "human_decision"
            )
        )


        if human_decision:

            st.markdown(
                "### Human-in-the-Loop Decision"
            )


            st.info(
                str(human_decision)
            )


        # ---------------------------------------------
        # Guardrail Status
        # ---------------------------------------------

        guardrail_status = (

            result.get(
                "guardrail_status"
            )

            or output.get(
                "guardrail_status"
            )
        )


        guardrail_reason = (

            result.get(
                "guardrail_reason"
            )

            or output.get(
                "guardrail_reason"
            )
        )


        if guardrail_status:

            st.markdown(
                "### Guardrail Status"
            )


            if (
                str(guardrail_status).upper()
                == "PASS"
            ):

                st.success(
                    "Guardrails: PASS"
                )

            else:

                st.error(
                    "Guardrails: "
                    + str(
                        guardrail_status
                    ).upper()
                )


            if guardrail_reason:

                st.caption(
                    "Reason: "
                    + str(
                        guardrail_reason
                    )
                )


        # ---------------------------------------------
        # Raw response
        # ---------------------------------------------

        with st.expander(
            "View Raw n8n Response"
        ):

            st.json(
                result
            )


    else:

        st.warning(
            "The workflow returned "
            "an unexpected response format."
        )


        with st.expander(
            "View Raw Response"
        ):

            st.write(
                result
            )


# =========================================================
# WORKFLOW DESCRIPTION
# =========================================================

st.divider()


st.subheader(
    "FraudGuard AI Workflow"
)


st.markdown(
    """
**Streamlit UI → n8n Webhook → Alert Validation → FraudGuard Investigator → Customer/Device/IP Evidence → Guardrails → Risk Routing → HITL for High Risk → Audit Logging**

### Risk Routing

- **Score < 40:** Lower-risk path
- **Score 40–69:** Medium-risk investigation path
- **Score ≥ 70:** High-risk path with human approval
- **Guardrail failure:** Human review / escalation
"""
)


st.caption(
    "FraudGuard AI is a functional educational PoC. "
    "High-risk decisions retain human oversight."
)
