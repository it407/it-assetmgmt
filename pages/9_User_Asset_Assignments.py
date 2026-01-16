# pages/9_User_Asset_Assignments.py

import streamlit as st
import pandas as pd
import duckdb

from utils.permissions import login_required, admin_only
from utils.gsheets import read_sheet
from utils.export import export_csv
from utils.constants import ASSET_ASSIGNMENTS_SHEET, ASSETS_MASTER_SHEET

# ─────────────────────────────────────────────
# Page protection
# ─────────────────────────────────────────────
from utils.permissions import admin_or_manager_only
admin_or_manager_only()
from utils.navigation import apply_role_based_navigation
apply_role_based_navigation()


st.title("User Assets Assignment")

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
assignments_df = read_sheet(ASSET_ASSIGNMENTS_SHEET)
assets_df = read_sheet(ASSETS_MASTER_SHEET)
employees_df = read_sheet("employee_master")

if assignments_df.empty:
    st.info("No asset assignments found.")
    st.stop()

# Normalize columns
for df in [assignments_df, assets_df, employees_df]:
    if not df.empty:
        df.columns = df.columns.str.strip().str.lower()

# ─────────────────────────────────────────────
# Keep only ACTIVE assignments
# ─────────────────────────────────────────────
assigned_df = assignments_df[
    assignments_df["assignment_status"] == "Assigned"
]

if assigned_df.empty:
    st.info("No active asset assignments.")
    st.stop()

# ─────────────────────────────────────────────
# DuckDB join (SAFE & EXPLICIT)
# ─────────────────────────────────────────────
con = duckdb.connect(database=":memory:")

con.register("assignments", assigned_df)
con.register("assets", assets_df)
con.register("employees", employees_df)

query = """
SELECT
    a.assignment_id,
    a.asset_id,
    am.asset_name,
    am.category,
    a.employee_id,
    a.employee_name,
    e.department,
    am.location,
    a.assigned_on
FROM assignments a
LEFT JOIN assets am
    ON a.asset_id = am.asset_id
LEFT JOIN employees e
    ON a.employee_id = e.employee_id
ORDER BY a.assigned_on DESC
"""

result_df = con.execute(query).df()

# ─────────────────────────────────────────────
# Filters
# ─────────────────────────────────────────────
st.subheader("🔎 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    emp_id_filter = st.multiselect(
        "Employee ID",
        sorted(result_df["employee_id"].dropna().unique().tolist()),
        default=sorted(result_df["employee_id"].dropna().unique().tolist())
    )

with col2:
    emp_name_filter = st.multiselect(
        "Employee Name",
        sorted(result_df["employee_name"].dropna().unique().tolist()),
        default=sorted(result_df["employee_name"].dropna().unique().tolist())
    )

with col3:
    dept_filter = st.multiselect(
        "Department",
        sorted(result_df["department"].dropna().unique().tolist()),
        default=sorted(result_df["department"].dropna().unique().tolist())
    )

with col4:
    location_filter = st.multiselect(
        "Location",
        sorted(result_df["location"].dropna().unique().tolist()),
        default=sorted(result_df["location"].dropna().unique().tolist())
    )

filtered_df = result_df[
    result_df["employee_id"].isin(emp_id_filter)
    & result_df["employee_name"].isin(emp_name_filter)
    & result_df["department"].isin(dept_filter)
    & result_df["location"].isin(location_filter)
]

# ─────────────────────────────────────────────
# Result table
# ─────────────────────────────────────────────
st.subheader("📋 Assigned Assets (Current)")

if filtered_df.empty:
    st.warning("No data for selected filters.")
else:
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    export_csv(filtered_df, "user_wise_assigned_assets.csv")
