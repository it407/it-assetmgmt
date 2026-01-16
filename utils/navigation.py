# utils/navigation.py

import streamlit as st
from utils.gsheets import read_sheet
from utils.constants import ROLE_ADMIN

def apply_role_based_navigation():
    user = st.session_state.get("user")
    if not user:
        return

    role = user["role"]

    # 🔒 CRITICAL: Admin should NEVER have nav filtered
    if role == ROLE_ADMIN:
        return

    nav_df = read_sheet("role_navigation")
    if nav_df.empty:
        return  # fail open

    nav_df.columns = nav_df.columns.str.strip().str.lower()

    nav_df["is_visible"] = (
        nav_df["is_visible"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    allowed_pages = nav_df[
        (nav_df["role"] == role)
        & (nav_df["is_visible"])
    ]["page_title"].tolist()

    # 🚨 NEVER blank sidebar
    if not allowed_pages:
        return

    selectors = "\n".join(
        [
            f'[data-testid="stSidebarNav"] a[aria-label="{p}"] {{ display: block !important; }}'
            for p in allowed_pages
        ]
    )

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebarNav"] li {{
            display: none;
        }}
        {selectors}
        </style>
        """,
        unsafe_allow_html=True,
    )
