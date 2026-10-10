import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="DNS Tunnel Detector", layout="wide")
st.title("🛡️ Real-Time DNS Tunneling Detector")

# Read alerts
def get_alerts():
    if not os.path.exists("results/live_alerts.txt"):
        return []
    with open("results/live_alerts.txt", "r") as f:
        lines = f.readlines()
    
    parsed = []
    for line in lines:
        if "[ALERT]" in line:
            parts = line.strip().split()
            if len(parts) >= 6:
                parsed.append({
                    "Time": parts[1],
                    "Client IP": parts[2],
                    "Probability": parts[3].replace("p=", ""),
                    "Latency": parts[4].replace("proc=", ""),
                    "Domain": parts[5]
                })
    return parsed

st.write("Monitoring `live_alerts.txt` for real-time exfiltration events...")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Live Alerts Log")
    alerts = get_alerts()
    if alerts:
        df = pd.DataFrame(alerts)
        st.dataframe(df, height=400)
    else:
        st.info("No alerts detected yet.")

with col2:
    st.subheader("Model Feature Importances")
    if os.path.exists("results/feature_importances.png"):
        st.image("results/feature_importances.png", use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    if os.path.exists("results/confusion_matrix.png"):
         st.image("results/confusion_matrix.png", use_container_width=True)
with col4:
    if os.path.exists("results/roc_curve.png"):
         st.image("results/roc_curve.png", use_container_width=True)

time.sleep(2)
st.rerun()
