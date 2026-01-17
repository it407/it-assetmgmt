# utils/permissions.py

import streamlit as st
from utils.auth import login
from utils.constants import ROLE_ADMIN, ROLE_MANAGER, ROLE_HR

def login_required():
    """
    HARD GATE:
    - If not logged in → show ONLY login UI and STOP the script.
    - Nothing else (nav/sidebar/pages) should render before login.
    """
    if "user" not in st.session_state:
        login()
        st.stop()  # 🔒 critical: prevents any further rendering

def admin_only():
    login_required()
    if st.session_state["user"]["role"] != ROLE_ADMIN:
        st.error("Admin access required")
        st.stop()

def admin_or_manager_only():
    login_required()
    if st.session_state["user"]["role"] not in [ROLE_ADMIN, ROLE_MANAGER]:
        st.error("Access restricted")
        st.stop()

def hr_only():
    login_required()
    if st.session_state["user"]["role"] != ROLE_HR:
        st.error("HR access required")
        st.stop()
