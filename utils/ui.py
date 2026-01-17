# utils/ui.py

import streamlit as st
from utils.constants import ROLE_ADMIN, ROLE_MANAGER, ROLE_USER, ROLE_HR

def back_to_home_button():
    """
    Standard Back button at top of pages.
    Redirects user based on role.
    """
    user = st.session_state.get("user")
    if not user:
        return

    role = user["role"]

    if st.button("⬅ Back"):
        if role in [ROLE_ADMIN, ROLE_MANAGER]:
            st.switch_page("app.py")
        elif role == ROLE_USER:
            st.switch_page("pages/5_My_Assets.py")
        elif role == ROLE_HR:
            st.switch_page("pages/11_Attendance_Dashboard.py")

        st.stop()  # critical
