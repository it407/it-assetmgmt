# utils/navigation.py

import streamlit as st
from utils.gsheets import read_sheet

def apply_role_based_navigation():
    user = st.session_state.get("user")
    if not user:
        return

    role = user["role"]

    nav_df = read_sheet("role_navigation")
    if nav_df.empty:
        return

    nav_df.columns = nav_df.columns.str.strip().str.lower()

    allowed_pages = nav_df[
        (nav_df["role"] == role)
        & (nav_df["is_visible"].astype(str).str.lower() == "true")
    ]["page_title"].tolist()

    if not allowed_pages:
        return

    # Build CSS allow-list
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
