# app.py

import streamlit as st
from utils.permissions import login_required
from utils.auth import logout
from utils.constants import ROLE_ADMIN

st.set_page_config(
    page_title="IT Asset & Subscription Manager",
    layout="wide"
)

# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────
login_required()
user = st.session_state["user"]

# ─────────────────────────────────────────────
# Sidebar header
# ─────────────────────────────────────────────
st.sidebar.success(f"Logged in as {user['email']} ({user['role']})")

# Logout button
logout()

# ─────────────────────────────────────────────
# ROLE-BASED SIDEBAR VISIBILITY (UI LEVEL)
# ─────────────────────────────────────────────
if user["role"] != ROLE_ADMIN:
    # Hide all pages except first one (My Assets)
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] li:not(:first-child) {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────
st.title("🏢 IT Asset & Subscription Management System")

if user["role"] == ROLE_ADMIN:
    st.markdown("""
    ### Welcome Admin 👋  
    You have full access to the system.

    Use the sidebar to manage:
    - Assets
    - Asset Assignments & Returns
    - Subscriptions
    - Reports & Dashboards
    """)
else:
    st.markdown("""
    ### Welcome 👋  
    You can view **only your assigned assets**.

    👉 Please use **My Assets** from the sidebar.
    """)

