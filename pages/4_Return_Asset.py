# pages/4_Return_Asset.py

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.permissions import login_required, admin_only
from utils.gsheets import read_sheet, write_sheet
from utils.constants import ASSET_ASSIGNMENTS_SHEET, ASSETS_MASTER_SHEET
from utils.auth import logout
logout()

# ─────────────────────────────────────────────
# Page protection
# ─────────────────────────────────────────────
login_required()
admin_only()

st.title("↩️ Return Asset")

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
assignments_df = read_sheet(ASSET_ASSIGNMENTS_SHEET)
assets_df = read_sheet(ASSETS_MASTER_SHEET)

if assignments_df.empty:
    st.info("No asset assignments found.")
    st.stop()

for df in [assignments_df, assets_df]:
    df.columns = df.columns.str.strip().str.lower()

active_assignments = assignments_df[
    assignments_df["assignment_status"] == "Assigned"
]

if active_assignments.empty:
    st.info("No active asset assignments.")
    st.stop()

# ─────────────────────────────────────────────
# Return form
# ─────────────────────────────────────────────
with st.form("return_asset_form"):
    assignment_option = st.selectbox(
        "Select Assignment",
        active_assignments.apply(
            lambda x: (
                f"{x['assignment_id']} | "
                f"{x['asset_id']} | "
                f"{x['employee_id']} | "
                f"{x['employee_name']}"
            ),
            axis=1
        )
    )

    return_reason = st.selectbox(
        "Return Reason *",
        [
            "Reassignment",
            "Employee Exit",
            "Asset Inactive / Damaged",
            "Other",
        ]
    )

    returned_on = st.date_input("Return Date", value=datetime.today())
    submit = st.form_submit_button("↩️ Return Asset")

# ─────────────────────────────────────────────
# Return logic
# ─────────────────────────────────────────────
if submit:
    assignment_id = assignment_option.split(" | ")[0]

    idx = assignments_df[
        assignments_df["assignment_id"] == assignment_id
    ].index

    if idx.empty:
        st.error("Assignment not found.")
        st.stop()

    asset_id = assignments_df.loc[idx[0], "asset_id"]

    assignments_df.loc[idx, "assignment_status"] = "Returned"
    assignments_df.loc[idx, "returned_on"] = returned_on.isoformat()
    assignments_df.loc[idx, "return_reason"] = return_reason

    if return_reason == "Asset Inactive / Damaged":
        assets_df.loc[
            assets_df["asset_id"] == asset_id, "is_active"
        ] = False
        assets_df.loc[
            assets_df["asset_id"] == asset_id, "updated_at"
        ] = datetime.now().date().isoformat()

    write_sheet(ASSET_ASSIGNMENTS_SHEET, assignments_df)
    write_sheet(ASSETS_MASTER_SHEET, assets_df)

    st.success("Asset returned successfully")
    st.rerun()

# ─────────────────────────────────────────────
# Active assignments table
# ─────────────────────────────────────────────
st.divider()
st.subheader("📌 Currently Assigned Assets")

st.dataframe(
    active_assignments.sort_values("assigned_on", ascending=False),
    use_container_width=True
)
