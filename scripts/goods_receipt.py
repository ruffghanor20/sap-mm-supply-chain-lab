"""
goods_receipt.py
Simulates SAP MM transaction MIGO - Goods Receipt against a Purchase Order.
"""

import pandas as pd
import os
from datetime import date

DATA_PATH_PO = os.path.join(
    os.path.dirname(__file__), "..", "data", "purchase_orders.csv"
)
DATA_PATH_INVENTORY = os.path.join(
    os.path.dirname(__file__), "..", "data", "inventory.csv"
)


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: str) -> None:
    """Persist a DataFrame to CSV."""
    df.to_csv(path, index=False)


def post_goods_receipt(
    po_number: str,
    gr_quantity: float,
    po_path: str = DATA_PATH_PO,
    inventory_path: str = DATA_PATH_INVENTORY,
) -> dict:
    """
    Post a goods receipt (GR) for an open purchase order.

    Parameters
    ----------
    po_number : str
        The purchase order number (e.g. PO-30007).
    gr_quantity : float
        Quantity received. Must not exceed the ordered quantity.
    po_path : str
        Path to the purchase orders CSV.
    inventory_path : str
        Path to the inventory CSV.

    Returns
    -------
    dict
        A summary of the goods receipt posting.
    """
    po_df = load_csv(po_path)
    inv_df = load_csv(inventory_path)

    po_mask = po_df["po_number"] == po_number
    if not po_mask.any():
        raise ValueError(f"Purchase Order '{po_number}' not found.")

    po_row = po_df[po_mask].iloc[0]

    if po_row["status"] == "COMPLETED":
        raise ValueError(f"Purchase Order '{po_number}' is already fully received.")

    ordered_qty = float(po_row["quantity"])
    already_received = float(po_row["gr_quantity"]) if pd.notna(po_row["gr_quantity"]) else 0.0

    if already_received + gr_quantity > ordered_qty:
        raise ValueError(
            f"GR quantity {gr_quantity} exceeds remaining open quantity "
            f"{ordered_qty - already_received:.2f}."
        )

    gr_date = date.today().isoformat()
    total_received = already_received + gr_quantity
    new_status = "COMPLETED" if total_received >= ordered_qty else "GR_DONE"

    po_df.loc[po_mask, "gr_quantity"] = total_received
    po_df.loc[po_mask, "gr_date"] = gr_date
    po_df.loc[po_mask, "status"] = new_status
    save_csv(po_df, po_path)

    material_id = int(po_row["material_id"])
    plant = po_row["plant"]
    storage_location = po_row["storage_location"]

    inv_mask = (
        (inv_df["material_id"] == material_id)
        & (inv_df["plant"] == plant)
        & (inv_df["storage_location"] == storage_location)
    )

    if inv_mask.any():
        inv_df.loc[inv_mask, "quantity"] = (
            inv_df.loc[inv_mask, "quantity"].values[0] + gr_quantity
        )
        inv_df.loc[inv_mask, "unrestricted_stock"] = (
            inv_df.loc[inv_mask, "unrestricted_stock"].values[0] + gr_quantity
        )
        inv_df.loc[inv_mask, "last_updated"] = gr_date
    else:
        new_inv_id = int(inv_df["inventory_id"].max()) + 1 if not inv_df.empty else 1
        new_inv = {
            "inventory_id": new_inv_id,
            "material_id": material_id,
            "material_number": po_row["material_number"],
            "plant": plant,
            "storage_location": storage_location,
            "quantity": gr_quantity,
            "unit_of_measure": po_row["unit_of_measure"],
            "unrestricted_stock": gr_quantity,
            "quality_inspection": 0.0,
            "blocked_stock": 0.0,
            "in_transit": 0.0,
            "valuation_price": float(po_row["net_price"]),
            "currency": po_row["currency"],
            "last_updated": gr_date,
        }
        inv_df = pd.concat([inv_df, pd.DataFrame([new_inv])], ignore_index=True)

    save_csv(inv_df, inventory_path)

    result = {
        "po_number": po_number,
        "material_number": po_row["material_number"],
        "gr_quantity": gr_quantity,
        "gr_date": gr_date,
        "po_status": new_status,
        "plant": plant,
        "storage_location": storage_location,
    }
    print(
        f"[MIGO] Goods Receipt posted: {gr_quantity} {po_row['unit_of_measure']} "
        f"for PO '{po_number}'. New PO status: {new_status}."
    )
    return result


if __name__ == "__main__":
    result = post_goods_receipt(po_number="PO-30007", gr_quantity=100.0)
    print(result)
