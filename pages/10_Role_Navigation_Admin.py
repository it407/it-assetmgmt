# pages/10_Role_Navigation_Admin.py

import streamlit as st
import pandas as pd
from utils.auth import logout
from utils.permissions import login_required, admin_only
from utils.gsheets import read_sheet, write_sheet

login_required()
admin_only()
logout()

st.title("Role Navigation Admin")

SHEET_NAME = "role_navigation"

# Load config
nav_df = read_sheet(SHEET_NAME)

if nav_df.empty:
    st.warning("Navigation config not found. Create entries first.")
    st.stop()

nav_df.columns = nav_df.columns.str.strip().str.lower()

st.info("Toggle which pages are visible for each role.")

# Editable table
edited_df = st.data_editor(
    nav_df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "is_visible": st.column_config.CheckboxColumn(
            "Visible"
        )
    }
)

if st.button("💾 Save Navigation Settings"):
    write_sheet(SHEET_NAME, edited_df)
    st.success("Navigation updated successfully")
