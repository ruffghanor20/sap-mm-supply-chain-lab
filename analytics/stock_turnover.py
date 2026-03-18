"""
stock_turnover.py
Calculates stock turnover ratio and days-on-hand for inventory items.

Stock Turnover Ratio = Cost of Goods Sold (COGS) / Average Inventory Value
Days on Hand        = 365 / Stock Turnover Ratio
"""

import pandas as pd
import os

DATA_PATH_INVENTORY = os.path.join(
    os.path.dirname(__file__), "..", "data", "inventory.csv"
)
DATA_PATH_PO = os.path.join(
    os.path.dirname(__file__), "..", "data", "purchase_orders.csv"
)
DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)


def load_data(
    inventory_path: str = DATA_PATH_INVENTORY,
    po_path: str = DATA_PATH_PO,
    materials_path: str = DATA_PATH_MATERIALS,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load inventory, purchase orders and materials data."""
    inv_df = pd.read_csv(inventory_path)
    po_df = pd.read_csv(po_path)
    mat_df = pd.read_csv(materials_path)
    return inv_df, po_df, mat_df


def calculate_stock_turnover(
    inventory_path: str = DATA_PATH_INVENTORY,
    po_path: str = DATA_PATH_PO,
    materials_path: str = DATA_PATH_MATERIALS,
    periods: int = 365,
) -> pd.DataFrame:
    """
    Calculate stock turnover metrics per material.

    The COGS is approximated from completed purchase orders (received goods value).
    Average inventory is the current on-hand value.

    Parameters
    ----------
    inventory_path : str
        Path to inventory CSV.
    po_path : str
        Path to purchase orders CSV.
    materials_path : str
        Path to materials CSV.
    periods : int
        Number of days in the analysis period (default 365 for annual).

    Returns
    -------
    pd.DataFrame
        Turnover metrics per material.
    """
    inv_df, po_df, mat_df = load_data(inventory_path, po_path, materials_path)

    completed_pos = po_df[po_df["status"].isin(["COMPLETED", "GR_DONE"])].copy()
    completed_pos["consumed_value"] = (
        completed_pos["gr_quantity"].fillna(0) * completed_pos["net_price"]
    )
    cogs_by_material = (
        completed_pos.groupby("material_number")["consumed_value"]
        .sum()
        .reset_index()
        .rename(columns={"consumed_value": "cogs"})
    )

    inv_df = inv_df.copy()
    inv_df["inventory_value"] = inv_df["unrestricted_stock"] * inv_df["valuation_price"]
    inv_value = (
        inv_df.groupby("material_number")["inventory_value"]
        .sum()
        .reset_index()
        .rename(columns={"inventory_value": "avg_inventory_value"})
    )

    mat_desc = mat_df[["material_number", "description", "unit_of_measure"]]
    result = mat_desc.merge(cogs_by_material, on="material_number", how="left")
    result = result.merge(inv_value, on="material_number", how="left")
    result["cogs"] = result["cogs"].fillna(0)
    result["avg_inventory_value"] = result["avg_inventory_value"].fillna(0)

    result["turnover_ratio"] = result.apply(
        lambda r: r["cogs"] / r["avg_inventory_value"]
        if r["avg_inventory_value"] > 0
        else 0,
        axis=1,
    )
    result["days_on_hand"] = result["turnover_ratio"].apply(
        lambda t: round(periods / t, 1) if t > 0 else float("inf")
    )

    result = result.sort_values("turnover_ratio", ascending=False).reset_index(drop=True)
    return result[
        [
            "material_number",
            "description",
            "cogs",
            "avg_inventory_value",
            "turnover_ratio",
            "days_on_hand",
        ]
    ]


if __name__ == "__main__":
    report = calculate_stock_turnover()
    print("\n=== Stock Turnover Analysis ===")
    pd.set_option("display.float_format", "{:,.2f}".format)
    print(report.to_string(index=False))
