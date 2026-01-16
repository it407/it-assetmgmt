import streamlit as st
import pandas as pd
from datetime import datetime
import re

from utils.permissions import login_required, admin_only
from utils.gsheets import read_sheet, append_row

# ─────────────────────────────────────────────
# Page protection
# ─────────────────────────────────────────────
login_required()
admin_only()

st.title("📡 CCTV / Wi-Fi Credentials Master")

SHEET_NAME = "cctv_wifi_credential"

# ─────────────────────────────────────────────
# Load existing credentials
# ─────────────────────────────────────────────
cred_df = read_sheet(SHEET_NAME)
if not cred_df.empty:
    cred_df.columns = cred_df.columns.str.strip().str.lower()

# ─────────────────────────────────────────────
# IP validation
# ─────────────────────────────────────────────
def is_valid_ip(ip: str) -> bool:
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return bool(re.match(pattern, ip))

# ─────────────────────────────────────────────
# Submission form
# ─────────────────────────────────────────────
with st.form("cctv_wifi_form"):
    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input("Location *")
        device_type = st.selectbox(
            "Device Type *",
            ["WiFi Router", "CCTV Camera", "NVR / DVR", "Switch", "Other"]
        )
        ssid = st.text_input("SSID / Device Name *")

    with col2:
        password = st.text_input("Password *")
        ip_address = st.text_input("IP Address (example: 192.168.2.249)")
        remarks = st.text_area("Remarks")

    submit = st.form_submit_button("➕ Save Credential")

# ─────────────────────────────────────────────
# Submit logic
# ─────────────────────────────────────────────
if submit:
    if not location or not device_type or not ssid or not password:
        st.error("Location, Device Type, SSID, and Password are required.")
        st.stop()

    if ip_address and not is_valid_ip(ip_address):
        st.error("Invalid IP address format")
        st.stop()

    # ✅ ONLY RELIABLE WAY TO SAVE IP AS STRING
    safe_ip = f'="{ip_address}"' if ip_address else ""

    append_row(
        SHEET_NAME,
        {
            "location": location,
            "device_type": device_type,
            "ssid": ssid,
            "password": password,
            "ip_address": safe_ip,   # 👈 FORMULA-BASED TEXT
            "remarks": remarks,
            "created_at": datetime.now().isoformat(),
        }
    )

    st.success("CCTV / Wi-Fi credential saved successfully")
    st.rerun()

# ─────────────────────────────────────────────
# Credentials table view
# ─────────────────────────────────────────────
st.divider()
st.subheader("📋 Stored CCTV / Wi-Fi Credentials")

if cred_df.empty:
    st.info("No credentials found.")
else:
    if "created_at" in cred_df.columns:
        display_df = cred_df.sort_values("created_at", ascending=False)
    else:
        display_df = cred_df.copy()

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.download_button(
        label="⬇ Download Credentials (CSV)",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="cctv_wifi_credentials.csv",
        mime="text/csv"
    )
