# utils/sidebar.py

import streamlit as st
from utils.constants import ROLE_ADMIN, ROLE_MANAGER, ROLE_USER, ROLE_HR

def render_sidebar():
    user = st.session_state.get("user")
    if not user:
        return

    role = user["role"]

    st.sidebar.markdown("### 📌 Navigation")

    # ───────── ADMIN ─────────
    if role == ROLE_ADMIN:
        if st.sidebar.button("🏠 Dashboard"):
            st.switch_page("app.py")

        if st.sidebar.button("📊 Asset Summary"):
            st.switch_page("pages/1_Dashboard.py")

        if st.sidebar.button("👥 User Assets"):
            st.switch_page("pages/9_User_Asset_Assignments.py")

        st.sidebar.divider()

        if st.sidebar.button("🖨️ Assets Master"):
            st.switch_page("pages/2_Assets.py")

        if st.sidebar.button("🔗 Assign Asset"):
            st.switch_page("pages/3_Assign_Asset.py")

        if st.sidebar.button("↩️ Return Asset"):
            st.switch_page("pages/4_Return_Asset.py")

        st.sidebar.divider()

        if st.sidebar.button("🧭 Role Navigation Admin"):
            st.switch_page("pages/10_Role_Navigation_Admin.py")

    # ───────── MANAGER ─────────
    elif role == ROLE_MANAGER:
        if st.sidebar.button("🏠 Dashboard"):
            st.switch_page("app.py")

        if st.sidebar.button("📊 Asset Summary"):
            st.switch_page("pages/1_Dashboard.py")

        if st.sidebar.button("👥 User Assets"):
            st.switch_page("pages/9_User_Asset_Assignments.py")

    # ───────── USER ─────────
    elif role == ROLE_USER:
        if st.sidebar.button("📋 My Assets"):
            st.switch_page("pages/5_My_Assets.py")

    # ───────── HR ─────────
    elif role == ROLE_HR:
        if st.sidebar.button("📊 Attendance"):
            st.switch_page("pages/11_Attendance_Dashboard.py")
