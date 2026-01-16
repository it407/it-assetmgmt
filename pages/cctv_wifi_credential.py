import streamlit as st
import pandas as pd
from datetime import datetime

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
# Safe credential_id generator
# Format: NET-001
# ─────────────────────────────────────────────
def get_next_credential_id(df: pd.DataFrame):
    if df.empty or "credential_id" not in df.columns:
        return "NET-001"

    nums = df["credential_id"].astype(str).str.extract(r"(\d+)")
    nums = nums.dropna()

    if nums.empty:
        return "NET-001"

    next_num = nums[0].astype(int).max() + 1
    return f"NET-{str(next_num).zfill(3)}"

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
        ip_address = st.text_input("IP Address")
        remarks = st.text_area("Remarks")

    submit = st.form_submit_button("➕ Save Credential")

# ─────────────────────────────────────────────
# Submit logic
# ─────────────────────────────────────────────
if submit:
    if not location or not device_type or not ssid or not password:
        st.error("Location, Device Type, SSID, and Password are required.")
        st.stop()

    credential_id = get_next_credential_id(cred_df)

    append_row(
        SHEET_NAME,
        {
            "credential_id": credential_id,
            "location": location,
            "device_type": device_type,
            "ssid": ssid,
            "password": password,
            "ip_address": ip_address,
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
    sorted_df = cred_df.sort_values("created_at", ascending=False)

    st.dataframe(
        sorted_df,
        use_container_width=True
    )

    # ⬇ CSV DOWNLOAD
    st.download_button(
        label="⬇ Download Credentials (CSV)",
        data=sorted_df.to_csv(index=False).encode("utf-8"),
        file_name="cctv_wifi_credentials.csv",
        mime="text/csv"
    )
