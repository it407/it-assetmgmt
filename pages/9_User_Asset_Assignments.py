import streamlit as st
import pandas as pd
import duckdb

from utils.permissions import admin_or_manager_only
from utils.gsheets import read_sheet
from utils.export import download_csv
from utils.ui import apply_global_ui
from utils.auth import logout

# ─────────────────────────────────────────────
# Global UI + Security
# ─────────────────────────────────────────────
apply_global_ui()
admin_or_manager_only()
logout()

# ─────────────────────────────────────────────
# Back to Dashboard Hub
# ─────────────────────────────────────────────
if st.button("⬅ Back to Dashboard"):
    st.switch_page("app.py")

st.title("👥 User Asset Assignments")

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
assignments = read_sheet("asset_assignments")
assets = read_sheet("assets_master")
employees = read_sheet("employee_master")

# Normalize columns
for df in [assignments, assets, employees]:
    df.columns = df.columns.str.strip().str.lower()

# Guard empty
if assignments.empty or assets.empty or employees.empty:
    st.warning("Required data is missing.")
    st.stop()

# ─────────────────────────────────────────────
# Filters UI
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    search_text = st.text_input(
        "🔍 Search Employee (ID or Name)",
        placeholder="EMP-001 or Nitesh"
    ).strip()

with col2:
    dept_options = ["All"] + sorted(
        employees["department"].dropna().unique().tolist()
    )
    department = st.selectbox("Department", dept_options)

with col3:
    loc_options = ["All"] + sorted(
        employees["location"].dropna().unique().tolist()
    )
    location = st.selectbox("Location", loc_options)

# ─────────────────────────────────────────────
# DuckDB Query (SAFE & EXPLICIT)
# ─────────────────────────────────────────────
query = """
SELECT
    a.assignment_id,
    a.asset_id,
    am.asset_name,
    am.category,
    e.employee_id,
    e.employee_name,
    e.department,
    e.location,
    a.assigned_on,
    a.assignment_status
FROM assignments a
JOIN assets am ON a.asset_id = am.asset_id
JOIN employees e ON a.employee_id = e.employee_id
WHERE a.assignment_status = 'Assigned'
"""

conditions = []
params = {}

if search_text:
    conditions.append(
        "(LOWER(e.employee_id) LIKE LOWER(:search) OR LOWER(e.employee_name) LIKE LOWER(:search))"
    )
    params["search"] = f"%{search_text}%"

if department != "All":
    conditions.append("e.department = :department")
    params["department"] = department

if location != "All":
    conditions.append("e.location = :location")
    params["location"] = location

if conditions:
    query += " AND " + " AND ".join(conditions)

result_df = duckdb.execute(
    query,
    params,
    tables={
        "assignments": assignments,
        "assets": assets,
        "employees": employees
    }
).df()

# ─────────────────────────────────────────────
# Display
# ─────────────────────────────────────────────
st.subheader("📋 Assigned Assets")

if result_df.empty:
    st.info("No records found.")
else:
    st.dataframe(result_df, use_container_width=True)

    # ─────────────────────────────────────────────
    # CSV Export
    # ─────────────────────────────────────────────
    download_csv(
        df=result_df,
        filename="user_asset_assignments.csv",
        label="⬇️ Download CSV"
    )
