# utils/navigation.py

import streamlit as st
from utils.constants import ROLE_ADMIN, ROLE_MANAGER

def apply_role_based_navigation():
    user = st.session_state.get("user")
    if not user:
        return

    role = user["role"]

    # USER → only My Assets
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

    # MANAGER → dashboards only
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

    # ADMIN → no restrictions
