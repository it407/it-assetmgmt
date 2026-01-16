# pages/5_My_Assets.py

import streamlit as st
import pandas as pd

from utils.permissions import login_required
from utils.gsheets import read_sheet
from utils.export import export_csv
from utils.constants import ASSET_ASSIGNMENTS_SHEET, ROLE_ADMIN

# ─────────────────────────────────────────────
# Page protection
# ─────────────────────────────────────────────
login_required()

user = st.session_state["user"]
employee_id = user["employee_id"]
is_admin = user["role"] == ROLE_ADMIN

st.title("🧑‍💻 My Assets")

# ─────────────────────────────────────────────
# Load assignments
# ─────────────────────────────────────────────
assignments_df = read_sheet(ASSET_ASSIGNMENTS_SHEET)

if assignments_df.empty:
    st.info("No asset assignments found.")
    st.stop()

assignments_df.columns = assignments_df.columns.str.strip().str.lower()

# ─────────────────────────────────────────────
# Filter logic (MANDATORY)
# ─────────────────────────────────────────────
if not is_admin:
    assignments_df = assignments_df[
        assignments_df["employee_id"] == employee_id
    ]

# ─────────────────────────────────────────────
# Show only current & past assignments
# ─────────────────────────────────────────────
current_assets = assignments_df[
    assignments_df["assignment_status"] == "Assigned"
]

past_assets = assignments_df[
    assignments_df["assignment_status"] == "Returned"
]

# ─────────────────────────────────────────────
# Current assets
# ─────────────────────────────────────────────
st.subheader("📌 Currently Assigned Assets")

if current_assets.empty:
    st.info("No active assets.")
else:
    st.dataframe(
        current_assets[
            [
                "assignment_id",
                "asset_id",
                "employee_name",
                "assigned_on",
                "remarks",
            ]
        ].sort_values("assigned_on", ascending=False),
        use_container_width=True,
    )

    export_csv(current_assets, "my_current_assets.csv")

# ─────────────────────────────────────────────
# Past assets
# ─────────────────────────────────────────────
st.divider()
st.subheader("📜 Assignment History")

if past_assets.empty:
    st.info("No past assets.")
else:
    st.dataframe(
        past_assets[
            [
                "assignment_id",
                "asset_id",
                "employee_name",
                "assigned_on",
                "returned_on",
                "return_reason",
            ]
        ].sort_values("returned_on", ascending=False),
        use_container_width=True,
    )

    export_csv(past_assets, "my_asset_history.csv")
