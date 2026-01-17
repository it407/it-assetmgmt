# utils/auth.py

import streamlit as st
from utils.gsheets import read_sheet
from utils.constants import USERS_SHEET

def login():
    # If already logged in, do nothing
    if "user" in st.session_state:
        return

    # Hide sidebar navigation during login screen
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔐 IT Asset Management Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = read_sheet(USERS_SHEET)

        if users.empty:
            st.error("User access table is empty")
            st.stop()

        # Normalize columns
        users.columns = users.columns.str.strip().str.lower()

        # Filter user
        user = users[
            (users["email"].astype(str).str.strip() == str(email).strip())
            & (users["password"].astype(str) == str(password))
            & (users["is_active"].astype(str).str.lower() == "true")
        ]

        if user.empty:
            st.error("Invalid credentials or inactive user")
            st.stop()

        st.session_state["user"] = {
            "user_id": str(user.iloc[0]["user_id"]).strip(),
            "employee_id": str(user.iloc[0]["employee_id"]).strip(),
            "email": str(user.iloc[0]["email"]).strip(),
            "role": str(user.iloc[0]["role"]).strip().upper(),  # ✅ makes Hr/HR safe
        }

        st.rerun()

def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
