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
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.success(f"Logged in as {user['email']} ({user['role']})")
logout()

# ─────────────────────────────────────────────
# HIDE PAGES FOR NON-ADMIN (FIXED)
# ─────────────────────────────────────────────
if user["role"] != ROLE_ADMIN:
    st.markdown(
        """
        <style>
        /* Hide all pages */
        [data-testid="stSidebarNav"] li {
            display: none;
        }

        /* Show ONLY My Assets */
        [data-testid="stSidebarNav"] li:has(a[title="My Assets"]) {
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

if user["role"] == ROLE_ADMIN:
    st.markdown("""
    ### Welcome Admin 👋  
    You have full access to the system.
    """)
else:
    st.markdown("""
    ### Welcome 👋  
    You can view **only your assigned assets**.

    👉 Please use **My Assets** from the sidebar.
    """)
