# pages/2_Assets.py

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.permissions import login_required, admin_only
from utils.gsheets import read_sheet, append_row
from utils.constants import ASSETS_MASTER_SHEET

# ─────────────────────────────────────────────
# Page protection
# ─────────────────────────────────────────────
login_required()
admin_only()

st.title("🖨️ Asset Submission (Unit-Based)")

# ─────────────────────────────────────────────
# Load existing assets
# ─────────────────────────────────────────────
assets_df = read_sheet(ASSETS_MASTER_SHEET)

if not assets_df.empty:
    assets_df.columns = assets_df.columns.str.strip().str.lower()

# ─────────────────────────────────────────────
# Helper: Generate next asset_id
# Format: AST-001
# ─────────────────────────────────────────────
def get_next_asset_ids(existing_df: pd.DataFrame, qty: int):
    if existing_df.empty:
        start = 1
    else:
        existing_df["num"] = (
            existing_df["asset_id"]
            .astype(str)
            .str.replace("AST-", "", regex=False)
            .astype(int)
        )
        start = existing_df["num"].max() + 1

    return [f"AST-{str(i).zfill(3)}" for i in range(start, start + qty)]

# ─────────────────────────────────────────────
# Asset submission form
# ─────────────────────────────────────────────
with st.form("asset_submission_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        asset_name = st.text_input("Asset Name *")
        category = st.text_input("Category *")
        brand = st.text_input("Brand")

    with col2:
        model = st.text_input("Model")
        location = st.text_input("Location *")
        qty = st.number_input("Quantity *", min_value=1, step=1)

    with col3:
        purchase_date = st.date_input("Purchase Date *")
        warranty_end = st.date_input("Warranty End Date *")
        is_active = st.selectbox("Is Active", [True, False])

    submitted = st.form_submit_button("➕ Create Assets")

# ─────────────────────────────────────────────
# Form validation & processing
# ─────────────────────────────────────────────
if submitted:
    if not asset_name or not category or not location:
        st.error("Asset Name, Category and Location are required")
        st.stop()

    now = datetime.today().date().isoformat()

    asset_ids = get_next_asset_ids(assets_df, qty)

    for asset_id in asset_ids:
        row = {
            "asset_id": asset_id,
            "asset_name": asset_name,
            "category": category,
            "brand": brand,
            "model": model,
            "purchase_date": purchase_date.isoformat(),
            "warranty_end": warranty_end.isoformat(),
            "location": location,
            "is_active": is_active,
            "created_at": now,
            "updated_at": now,
        }
        append_row(ASSETS_MASTER_SHEET, row)

    st.success(f"{qty} asset units created successfully")
    st.rerun()

# ─────────────────────────────────────────────
# View existing assets
# ─────────────────────────────────────────────
st.divider()
st.subheader("📋 Asset Inventory (Unit Level)")

if assets_df.empty:
    st.info("No assets found")
else:
    st.dataframe(
        assets_df.sort_values("asset_id"),
        use_container_width=True
    )
