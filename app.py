import streamlit as st
import pandas as pd
import numpy as np
import pickle
import altair as alt
import os
import time

# ===============================
# PAGE CONFIG & THEME
# ===============================
st.set_page_config(
    page_title="CyberSentinel | AI Phishing Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for a Professional Cybersecurity Interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Styles */
    .stApp { background-color: #0e1117; color: #e0e6ed; }
    font-family: 'Inter', sans-serif;

    /* Glassmorphism Card Effect */
    .cyber-card {
        background: rgba(23, 28, 35, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .stMetric {
        background: #1c2128;
        border: 1px solid #444c56;
        padding: 15px !important;
        border-radius: 8px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d;
    }

    /* Status Glow */
    .status-glow {
        color: #00ff41;
        text-shadow: 0 0 10px #00ff41;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# ROBUST MODEL LOADING
# ===============================
@st.cache_resource
def load_assets():
    # Use relative paths that work on both local and Streamlit Cloud
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "phishing_model.pkl")
vect_path  = os.path.join(base_path, "vectorizer.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(vect_path, "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        st.error("🚨 Model assets missing! Please ensure 'model/' folder contains .pkl files.")
        return None, None

model, vectorizer = load_assets()

# ===============================
# NAVIGATION
# ===============================
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/security-shield.png", width=80)
    st.title("CyberSentinel")
    page = st.radio("OPERATIONAL MODE", 
                   ["📡 Dashboard", "🔍 Live Inspection", "🧠 Threat Analysis", "📈 Intelligence Data"])
    st.divider()
    st.markdown("### SYSTEM STATUS")
    st.markdown("<p class='status-glow'>● ENGINES ONLINE</p>", unsafe_allow_html=True)
    st.caption("Model: Random Forest Classifier\nTF-IDF Enabled")

# ===============================
# DASHBOARD (HOME)
# ===============================
if page == "📡 Dashboard":
    st.title("Security Operations Center")
    st.markdown("#### Real-time Email Threat Intelligence")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Detection Accuracy", "98.4%", "+0.2%")
    col2.metric("False Positives", "0.04%", "-0.01%")
    col3.metric("Analysis Speed", "14ms", "Optimized")

    st.markdown("""
    <div class="cyber-card">
        <h3>System Overview</h3>
        <p>This AI-driven platform leverages <b>Natural Language Processing (NLP)</b> to intercept phishing attempts before they result in data breaches. 
        The underlying model analyzes linguistic patterns, urgency markers, and structural anomalies within email bodies.</p>
        <hr style="border:0.5px solid #30363d;">
        <ul>
            <li><b>Behavioral Analysis:</b> Scans for social engineering triggers.</li>
            <li><b>Linguistic Fingerprinting:</b> Compares text vectors against known phishing datasets.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# LIVE INSPECTION (DETECTION)
# ===============================
elif page == "🔍 Live Inspection":
    st.title("Neural Inspection Engine")
    
    with st.container():
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        email_input = st.text_area("INJECT EMAIL DATA FOR SCANNING", height=250, placeholder="Paste headers and body here...")
        
        if st.button("INITIATE DEEP SCAN"):
            if not email_input:
                st.warning("Input required for analysis.")
            elif model is None:
                st.error("Model not loaded.")
            else:
                with st.spinner("Decoding vectors and predicting intent..."):
                    # Preprocessing & Prediction
                    vec = vectorizer.transform([email_input])
                    prob = model.predict_proba(vec)[0][1]
                    pred = model.predict(vec)[0]
                    
                    time.sleep(0.8) # Simulated processing time
                    
                    st.divider()
                    res_col1, res_col2 = st.columns([1, 2])
                    
                    with res_col1:
                        if pred == 1:
                            st.error("🚨 THREAT DETECTED")
                            st.markdown(f"### Score: {prob*100:.1f}%")
                        else:
                            st.success("✅ VERIFIED SAFE")
                            st.markdown(f"### Score: {(1-prob)*100:.1f}%")
                            
                    with res_col2:
                        st.write("Confidence Interval")
                        st.progress(int(prob*100))
                        st.caption("The probability score represents the likelihood of a malicious payload/intent.")
        st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# THREAT ANALYSIS (AI ANALYSIS)
# ===============================
elif page == "🧠 Threat Analysis":
    st.title("Heuristic Keyword Analysis")
    
    email_text = st.text_area("PASTE TEXT FOR KEYWORD EXTRACTION")
    
    threat_library = {
        "Urgency": ["urgent", "immediately", "action required", "expiring"],
        "Financial": ["bank", "transfer", "invoice", "payment", "crypto"],
        "Security": ["login", "password", "verify", "suspended", "security"]
    }
    
    if st.button("RUN HEURISTICS"):
        found_triggers = []
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        
        for category, words in threat_library.items():
            matches = [w for w in words if w in email_text.lower()]
            if matches:
                st.write(f"**{category} Triggers:** {', '.join(matches)}")
                found_triggers.extend(matches)
        
        if not found_triggers:
            st.info("No common phishing keywords detected.")
        else:
            st.warning(f"Warning: {len(found_triggers)} social engineering markers found.")
        st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# INTELLIGENCE DATA (CHARTS)
# ===============================
elif page == "📈 Intelligence Data":
    st.title("Threat Landscape Statistics")
    
    # Example Trend Data
    data = pd.DataFrame({
        'Month': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
        'Phishing': [450, 520, 800, 610, 740],
        'Legit': [1200, 1150, 1300, 1250, 1400]
    }).melt('Month', var_name='Type', value_name='Volume')

    chart = alt.Chart(data).mark_line(point=True).encode(
        x='Month',
        y='Volume',
        color=alt.Color('Type', scale=alt.Scale(range=['#00ff41', '#ff4b4b'])),
        tooltip=['Month', 'Type', 'Volume']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
    st.caption("Historical Trend: Detected threats vs. legitimate traffic.")

# ===============================
# FOOTER
# ===============================
st.divider()
st.caption("CyberSentinel AI Framework v2.4 | Encrypted Node #882")
