import streamlit as st
import re
from urllib.parse import urlparse

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="centered"
)

# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Application heading
st.title("🛡️ CYBERSHIELD AI")
st.subheader("Intelligent Scam Detection Chatbot")

st.write(
    "Analyse suspicious SMS, emails and website links "
    "using CyberShield AI."
)

st.divider()

# Message input
message = st.text_area("Enter your suspicious message or URL:")

if st.button("🔍 Analyse Message"):

    if not message.strip():
        st.warning("Please enter a message.")

    else:
        text = message.lower()
        detected = []

        suspicious_words = [
            "free prize", "won", "winner", "urgent",
            "click here", "verify account", "otp",
            "bank details", "password", "claim now",
            "limited offer", "account blocked",
            "send money", "lottery"
        ]

        # Suspicious phrase detection
        for word in suspicious_words:
            if word in text:
                detected.append("Suspicious phrase: " + word)

        # URL detection
        urls = re.findall(r'https?://\S+|www\.\S+', text)

        for url in urls:
            url = url.rstrip(".,!?;:)")

            if url.startswith("www."):
                url = "http://" + url

            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            if parsed.scheme == "http":
                detected.append("Website uses HTTP instead of HTTPS")

            if any(char.isdigit() for char in domain):
                detected.append("URL contains unusual numbers")

            if len(domain) > 30:
                detected.append("Unusually long website address")

        # Risk score
        score = min(len(detected) * 25, 100)

        if score >= 50:
            risk = "HIGH RISK 🔴"
        elif score >= 25:
            risk = "MEDIUM RISK 🟠"
        else:
            risk = "LOW RISK 🟢"

        # Save analysis in history
        result = {
            "message": message,
            "score": score,
            "risk": risk,
            "warnings": detected
        }

        st.session_state.history.append(result)

# Display latest result
if st.session_state.history:

    latest = st.session_state.history[-1]

    st.divider()
    st.subheader("📊 Latest Analysis")

    st.write("Risk Level:", latest["risk"])
    st.progress(latest["score"] / 100)
    st.write("Risk Score:", latest["score"], "/100")

    if latest["warnings"]:
        st.write("Warning Signs:")
        for warning in latest["warnings"]:
            st.write("⚠️", warning)
    else:
        st.success("No known warning patterns detected.")

    st.info(
        "Safety Advice: Never share OTPs or passwords. "
        "Avoid suspicious links and verify messages "
        "through official channels."
    )
    # Risk Dashboard
st.divider()
st.header("📊 CyberShield AI Risk Dashboard")

if st.session_state.history:

    total = len(st.session_state.history)

    high = sum(
        1 for item in st.session_state.history
        if "HIGH RISK" in item["risk"]
    )

    medium = sum(
        1 for item in st.session_state.history
        if "MEDIUM RISK" in item["risk"]
    )

    low = sum(
        1 for item in st.session_state.history
        if "LOW RISK" in item["risk"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Messages", total)
        st.metric("High Risk 🔴", high)

    with col2:
        st.metric("Medium Risk 🟠", medium)
        st.metric("Low Risk 🟢", low)

    st.subheader("Risk Distribution")

    chart_data = {
        "Number of Messages": [high, medium, low]
    }

    st.bar_chart(chart_data)

else:
    st.info("Analyse messages to generate dashboard statistics.")

# Chat history
st.divider()
st.subheader("💬 Chat History")

if st.session_state.history:

    for index, item in enumerate(
        reversed(st.session_state.history), 1
    ):
        with st.expander(f"Analysis {index}: {item['risk']}"):
            st.write("Message:", item["message"])
            st.write("Risk Score:", item["score"], "/100")

            for warning in item["warnings"]:
                st.write("⚠️", warning)

else:
    st.write("No previous messages yet.")

st.caption(
    "CyberShield AI is an educational prototype. "
    "A low-risk result does not guarantee safety."
)