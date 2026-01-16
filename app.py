# app.py

import streamlit as st
from utils.permissions import login_required
from utils.auth import logout
from utils.constants import ROLE_ADMIN, ROLE_MANAGER

st.set_page_config(
    page_title="IT Asset & Subscription Manager",
    layout="wide"
)

# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────
login_required()
user = st.session_state["user"]
role = user["role"]

# ─────────────────────────────────────────────
# 🔁 AUTO-REDIRECT USER TO MY ASSETS
# ─────────────────────────────────────────────
if role == "User":
    if st.session_state.get("_redirected") != True:
        st.session_state["_redirected"] = True
        st.switch_page("pages/5_My_Assets.py")

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.success(f"Logged in as {user['email']} ({role})")
logout()

# ─────────────────────────────────────────────
# ROLE-BASED SIDEBAR VISIBILITY
# ─────────────────────────────────────────────
if role == "User":
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] li {
            display: none;
        }
        [data-testid="stSidebarNav"] li:has(a[title="My Assets"]) {
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

elif role == ROLE_MANAGER:
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] li {
            display: none;
        }
        [data-testid="stSidebarNav"] li:has(a[title*="Dashboard"]) {
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────
st.title("🏢 IT Asset & Subscription Management System")

if role == ROLE_ADMIN:
    st.markdown("### Welcome Admin 👋")
elif role == ROLE_MANAGER:
    st.markdown("### Welcome Manager 👋 (Dashboard Access)")
else:
    st.markdown("### Redirecting to My Assets…")
