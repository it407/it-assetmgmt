# app.py

import streamlit as st
from utils.permissions import login_required
from utils.auth import logout
from utils.navigation import apply_role_based_navigation
from utils.constants import ROLE_ADMIN, ROLE_MANAGER

st.set_page_config(
    page_title="IT Asset & Subscription Manager",
    layout="wide"
)

login_required()
apply_role_based_navigation()

user = st.session_state["user"]
role = user["role"]

st.sidebar.success(f"Logged in as {user['email']} ({role})")
logout()

# Auto-redirect user to My Assets
if role == "User" and not st.session_state.get("_redirected"):
    st.session_state["_redirected"] = True
    st.switch_page("pages/5_My_Assets.py")

st.title("🏢 IT Asset & Subscription Management System")

if role == ROLE_ADMIN:
    st.markdown("### Welcome Admin 👋")
elif role == ROLE_MANAGER:
    st.markdown("### Welcome Manager 👋 (Dashboard Access)")
else:
    st.markdown("### Redirecting to My Assets…")
