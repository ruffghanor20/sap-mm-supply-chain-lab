"""
inventory_report.py
Generates inventory reports similar to SAP MM transaction MB52 / MMBE.
"""

import pandas as pd
import os

DATA_PATH_INVENTORY = os.path.join(
    os.path.dirname(__file__), "..", "data", "inventory.csv"
)
DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)


def load_inventory(
    inventory_path: str = DATA_PATH_INVENTORY,
    materials_path: str = DATA_PATH_MATERIALS,
) -> pd.DataFrame:
    """Load and merge inventory with material master data."""
    inv_df = pd.read_csv(inventory_path)
    mat_df = pd.read_csv(materials_path)[["material_id", "description", "material_type", "material_group"]]
    return inv_df.merge(mat_df, on="material_id", how="left")


def stock_overview(
    plant: str = None,
    storage_location: str = None,
    inventory_path: str = DATA_PATH_INVENTORY,
    materials_path: str = DATA_PATH_MATERIALS,
) -> pd.DataFrame:
    """
    Return a stock overview (MMBE-style) optionally filtered by plant/storage location.

    Parameters
    ----------
    plant : str, optional
        Filter by plant code.
    storage_location : str, optional
        Filter by storage location code.
    inventory_path : str
        Path to inventory CSV.
    materials_path : str
        Path to materials CSV.

    Returns
    -------
    pd.DataFrame
        Stock overview with valuated amounts.
    """
    df = load_inventory(inventory_path, materials_path)

    if plant:
        df = df[df["plant"] == plant]
    if storage_location:
        df = df[df["storage_location"] == storage_location]

    df = df.copy()
    df["total_value"] = df["unrestricted_stock"] * df["valuation_price"]

    report = df[
        [
            "material_number",
            "description",
            "plant",
            "storage_location",
            "unrestricted_stock",
            "quality_inspection",
            "blocked_stock",
            "in_transit",
            "quantity",
            "unit_of_measure",
            "valuation_price",
            "total_value",
            "currency",
            "last_updated",
        ]
    ].sort_values("material_number")

    return report


def low_stock_alert(
    threshold_pct: float = 0.20,
    inventory_path: str = DATA_PATH_INVENTORY,
    materials_path: str = DATA_PATH_MATERIALS,
) -> pd.DataFrame:
    """
    Identify materials whose unrestricted stock is below a given percentage of total quantity.

    Parameters
    ----------
    threshold_pct : float
        Fraction of total quantity below which a stock alert is raised (default 20%).
    inventory_path : str
        Path to inventory CSV.
    materials_path : str
        Path to materials CSV.

    Returns
    -------
    pd.DataFrame
        Materials with low stock.
    """
    df = load_inventory(inventory_path, materials_path)
    df = df.copy()
    df["stock_pct"] = df["unrestricted_stock"] / df["quantity"].replace(0, float("nan"))
    alert_df = df[df["stock_pct"] < threshold_pct][
        ["material_number", "description", "plant", "storage_location",
         "unrestricted_stock", "quantity", "unit_of_measure", "stock_pct"]
    ]
    return alert_df


def print_report(df: pd.DataFrame, title: str = "Inventory Report") -> None:
    """Print a formatted inventory report to stdout."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")
    print(df.to_string(index=False))
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    overview = stock_overview()
    print_report(overview, "Stock Overview (MMBE)")

    alerts = low_stock_alert(threshold_pct=0.30)
    if not alerts.empty:
        print_report(alerts, "Low Stock Alert")
    else:
        print("No low-stock alerts.")
