import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(page_title="CCTV & WiFi Credential Manager", layout="wide")

# ================= UI CLEAN =================
st.markdown("""
<style>
.block-container { padding-top: 1rem; }
header [data-testid="stToolbar"] { display: none; }
a[href*="share.streamlit"],
[data-testid="stShareButton"] { display: none !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ================= SESSION INIT =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.employee_id = None
    st.session_state.role = None

# ================= GOOGLE SHEET CONFIG =================
SHEET_ID = "1FVjiK9Y-AhrogECD6Q8tRZpPiSxOFMevlMKGQWTGsHI"

ACCESS_SHEET = "user_access_master"
DATA_SHEET = "cctv_wifi_credential"

ACCESS_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={ACCESS_SHEET}"
DATA_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={DATA_SHEET}"

# ================= LOAD USERS (BULLETPROOF) =================
@st.cache_data(ttl=600)
def load_users():
    df = pd.read_csv(ACCESS_CSV_URL)

    # Handle broken headers (space separated)
    if len(df.columns) == 1:
        df = df.iloc[:, 0].astype(str).str.split(r"\s+", expand=True)
        df.columns = ["user_id", "employee_id", "username", "password", "role", "is_active"]

    # Normalize headers
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "")

    rename_map = {
        "userid": "user_id",
        "employeeid": "employee_id",
        "username": "username",
        "password": "password",
        "role": "role",
        "isactive": "is_active",
        "active": "is_active"
    }
    df = df.rename(columns=rename_map)

    df["is_active"] = df["is_active"].astype(str).str.upper() == "TRUE"

    return df

users_df = load_users()

# ================= LOAD CCTV / WIFI DATA =================
@st.cache_data(ttl=600)
def load_credentials():
    df = pd.read_csv(DATA_CSV_URL)

    # Normalize headers
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df

# ================= LOGIN SCREEN =================
def login_screen():
    st.title("🔐 Credential Manager Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users_df[
            (users_df["username"] == username) &
            (users_df["password"] == password) &
            (users_df["is_active"] == True)
        ]

        if user.empty:
            st.error("❌ Invalid credentials or inactive user")
        else:
            st.session_state.logged_in = True
            st.session_state.employee_id = user.iloc[0]["employee_id"]
            st.session_state.role = user.iloc[0]["role"]
            st.rerun()

# ================= LOGOUT =================
def logout_sidebar():
    with st.sidebar:
        st.markdown(f"👤 **Role:** {st.session_state.role}")
        st.markdown(f"🆔 **Employee ID:** {st.session_state.employee_id}")
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

# ================= AUTH GATE =================
if not st.session_state.logged_in:
    login_screen()
    st.stop()

logout_sidebar()

# ================= LOAD DATA =================
df = load_credentials()

st.title("📡 CCTV & WiFi Credential Manager")

if df.empty:
    st.warning("No credential data found.")
    st.stop()

# ================= ROLE NOTICE =================
if st.session_state.role != "Admin":
    st.info("🔒 View-only access (Admin can manage credentials)")

# ================= SEARCH =================
search = st.text_input("🔍 Search (Location / Device / SSID / IP)")

if search:
    df = df[df.apply(
        lambda row: search.lower() in " ".join(row.astype(str)).lower(),
        axis=1
    )]

# ================= MASK PASSWORDS FOR USERS =================
display_df = df.copy()

if st.session_state.role != "Admin":
    for col in display_df.columns:
        if "password" in col:
            display_df[col] = "••••••••"

# ================= TABLE =================
st.subheader("📋 Credential Records")
st.dataframe(display_df, use_container_width=True, height=520)

# ================= DOWNLOAD =================
st.download_button(
    "⬇ Download CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="cctv_wifi_credentials.csv",
    mime="text/csv"
)
