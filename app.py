# ===============================
# REQUIRED LIBRARIES
# ===============================
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import altair as alt
import re

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="AI Email Phishing Detector", layout="wide")

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    model = pickle.load(open("phishing_model.pkl","rb"))
    vectorizer = pickle.load(open("vectorizer.pkl","rb"))
    return model, vectorizer

model, vectorizer = load_model()

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>
body{
background-color:#f4f6fb;
}
.card{
background:white;
border-radius:15px;
padding:25px;
box-shadow:0px 5px 15px rgba(0,0,0,0.1);
margin-bottom:25px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
page = st.sidebar.radio(
"Navigation",
["Home","Live Detection","AI Security Scan","Security Dashboard","About"]
)

# ===============================
# HOME
# ===============================
if page == "Home":

    st.title("📧 AI Email Phishing Detection System")

    st.write("""
This application detects phishing emails using machine learning and AI based analysis.

The system evaluates:

• Machine learning phishing prediction  
• Suspicious keyword detection  
• URL analysis  
• Domain analysis  
• AI risk scoring
""")

# ===============================
# LIVE DETECTION
# ===============================
elif page == "Live Detection":

    st.title("🔍 Email Phishing Detection")

    email_text = st.text_area("Paste Email Content")

    if st.button("Analyze Email"):

        email_vector = vectorizer.transform([email_text])

        prediction = model.predict(email_vector)[0]

        probability = model.predict_proba(email_vector)[0][1]

        st.subheader("Detection Result")

        st.progress(int(probability*100))

        st.metric("Phishing Probability", f"{probability:.2f}")

        if prediction == 1:
            st.error("⚠ PHISHING EMAIL DETECTED")
        else:
            st.success("✅ SAFE EMAIL")

# ===============================
# AI SECURITY SCAN
# ===============================
elif page == "AI Security Scan":

    st.title("🧠 Advanced AI Security Analysis")

    email_text = st.text_area("Paste Email For AI Scan")

    if st.button("Run AI Scan"):

        email_vector = vectorizer.transform([email_text])

        probability = model.predict_proba(email_vector)[0][1]

        # Suspicious keywords
        suspicious_words = [
            "verify","password","bank","login","urgent",
            "click","account","update","confirm",
            "security","limited","alert","immediately"
        ]

        detected_words = []

        for word in suspicious_words:
            if word in email_text.lower():
                detected_words.append(word)

        # URL detection
        urls = re.findall(r'https?://\S+', email_text)

        # Domain detection
        domains = re.findall(r'@([a-zA-Z0-9.-]+)', email_text)

        # Risk score
        risk_score = probability*100
        risk_score += len(detected_words)*4
        risk_score += len(urls)*6

        if risk_score > 100:
            risk_score = 100

        st.subheader("AI Risk Score")

        st.progress(int(risk_score))

        if risk_score < 30:
            st.success("🟢 LOW RISK EMAIL")

        elif risk_score < 70:
            st.warning("🟠 SUSPICIOUS EMAIL")

        else:
            st.error("🔴 HIGH RISK PHISHING EMAIL")

        # Keyword display
        st.subheader("⚠ Suspicious Keywords")

        if detected_words:
            st.write(detected_words)
        else:
            st.write("No suspicious words detected")

        # URL report
        st.subheader("🔗 Links Found")

        if urls:
            st.write(urls)
        else:
            st.write("No links detected")

        # Domain report
        st.subheader("🌐 Domains Detected")

        if domains:
            st.write(domains)
        else:
            st.write("No domain detected")

        # AI Explanation
        st.subheader("🤖 AI Explanation")

        explanation = []

        if probability > 0.6:
            explanation.append("Machine learning model predicts phishing pattern")

        if detected_words:
            explanation.append("Suspicious phishing keywords detected")

        if urls:
            explanation.append("Email contains external links")

        if domains:
            explanation.append("Domain information detected")

        for e in explanation:
            st.write("•",e)

# ===============================
# SECURITY DASHBOARD
# ===============================
elif page == "Security Dashboard":

    st.title("📊 Phishing Analytics Dashboard")

    data = pd.DataFrame({
        "Category":["Phishing","Legitimate"],
        "Emails":[65,35]
    })

    chart = alt.Chart(data).mark_bar().encode(
        x="Category",
        y="Emails",
        color="Category"
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("Dashboard shows distribution of phishing vs legitimate emails.")

# ===============================
# ABOUT
# ===============================
elif page == "About":

    st.title("About Project")

    st.write("""
This project demonstrates a machine learning system for phishing email detection.

Main components:

• TF-IDF Feature Extraction  
• Machine Learning Classification  
• AI Security Analysis  
• Interactive Streamlit Dashboard
""")
