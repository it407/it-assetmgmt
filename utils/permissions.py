# utils/permissions.py

import streamlit as st
from utils.auth import login
from utils.constants import ROLE_ADMIN

def login_required():
    if "user" not in st.session_state:
        login()
        st.stop()

def admin_only():
    login_required()
    if st.session_state["user"]["role"] != ROLE_ADMIN:
        st.error("Admin access required")
        st.stop()
