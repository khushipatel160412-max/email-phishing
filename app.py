# ===============================
# REQUIRED LIBRARIES
# ===============================
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import altair as alt
from PIL import Image

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="AI Email Phishing Detector", layout="wide")

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    try:
        model = pickle.load(open("phishing_model.pkl","rb"))
        vectorizer = pickle.load(open("vectorizer.pkl","rb"))
        return model, vectorizer
    except:
        st.error("Model files not found. Please upload phishing_model.pkl and vectorizer.pkl")
        return None, None

model, vectorizer = load_model()

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>

body{
background-color:#f5f7fb;
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
["Home","Live Detection","AI Analysis","Charts","About"]
)

# ===============================
# HOME
# ===============================
if page == "Home":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("📧 AI Email Phishing Detection System")

    st.write("""
This application detects phishing emails using machine learning.

The model analyzes email content and predicts whether the email is:

• Legitimate Email  
• Phishing Email  

The system uses **TF-IDF feature extraction** and **ML classification**.
""")

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# LIVE DETECTION
# ===============================
elif page == "Live Detection":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("🔍 Email Phishing Detection")

    email_text = st.text_area("Paste Email Content")

    if st.button("Analyze Email"):

        if email_text == "":
            st.warning("Please enter email text")

        else:
            email_vector = vectorizer.transform([email_text])

            prediction = model.predict(email_vector)[0]

            probability = model.predict_proba(email_vector)[0][1]

            st.subheader("Detection Result")

            st.progress(int(probability*100))

            st.metric("Phishing Probability", f"{probability:.2f}")

            if prediction == 1:
                st.error("⚠️ PHISHING EMAIL DETECTED")
            else:
                st.success("✅ SAFE EMAIL")

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# AI ANALYSIS
# ===============================
elif page == "AI Analysis":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("🧠 Suspicious Keyword Detection")

    suspicious_words = [
        "verify",
        "password",
        "bank",
        "login",
        "urgent",
        "click",
        "account",
        "update"
    ]

    email_text = st.text_area("Paste Email Content For Keyword Scan")

    if st.button("Scan Email"):

        found_words = []

        for word in suspicious_words:
            if word in email_text.lower():
                found_words.append(word)

        if len(found_words) > 0:

            st.warning("⚠️ Suspicious Keywords Found")

            st.write(found_words)

        else:

            st.success("No suspicious keywords detected")

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# CHARTS
# ===============================
elif page == "Charts":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("📊 Phishing Statistics")

    chart_data = pd.DataFrame({
        "Email Type":["Phishing","Legitimate"],
        "Count":[60,40]
    })

    chart = alt.Chart(chart_data).mark_bar().encode(
        x="Email Type",
        y="Count"
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# ABOUT
# ===============================
elif page == "About":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("About This Project")

    st.write("""
This project uses machine learning to detect phishing emails.

Project Steps:

1. Data Collection  
2. Data Cleaning  
3. TF-IDF Feature Extraction  
4. Model Training  
5. Email Classification  

The model predicts whether an email is phishing or legitimate.
""")

    st.markdown("</div>", unsafe_allow_html=True)
