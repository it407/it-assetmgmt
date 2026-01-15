# app.py

import streamlit as st
from utils.permissions import login_required

st.set_page_config(
    page_title="IT Asset & Subscription Manager",
    layout="wide"
)

login_required()

user = st.session_state["user"]

st.sidebar.success(f"Logged in as {user['email']} ({user['role']})")

st.title("🏢 IT Asset & Subscription Management System")

st.markdown("""
Welcome to the internal IT system.

Use the sidebar to navigate:
- Assets
- Assignments
- Subscriptions
- Returns
""")
