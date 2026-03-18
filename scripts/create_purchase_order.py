"""
create_purchase_order.py
Simulates SAP MM transaction ME21N - Create Purchase Order.
"""

import pandas as pd
import os
from datetime import date, timedelta

DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)
DATA_PATH_VENDORS = os.path.join(
    os.path.dirname(__file__), "..", "data", "vendors.csv"
)
DATA_PATH_PO = os.path.join(
    os.path.dirname(__file__), "..", "data", "purchase_orders.csv"
)


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path)


def save_purchase_orders(df: pd.DataFrame, path: str = DATA_PATH_PO) -> None:
    """Persist the purchase orders DataFrame to CSV."""
    df.to_csv(path, index=False)


def create_purchase_order(
    vendor_number: str,
    material_number: str,
    quantity: float,
    net_price: float = None,
    currency: str = "USD",
    delivery_days: int = 30,
    plant: str = "PL01",
    storage_location: str = "SL01",
    vendors_path: str = DATA_PATH_VENDORS,
    materials_path: str = DATA_PATH_MATERIALS,
    po_path: str = DATA_PATH_PO,
) -> dict:
    """
    Create a new purchase order.

    Parameters
    ----------
    vendor_number : str
        Vendor number (e.g. VND-20001).
    material_number : str
        Material number to order.
    quantity : float
        Order quantity.
    net_price : float
        Price per unit. If None, the standard price from material master is used.
    currency : str
        Currency code, default 'USD'.
    delivery_days : int
        Number of days from today for expected delivery.
    plant : str
        Plant code.
    storage_location : str
        Storage location.
    vendors_path : str
        Path to vendors CSV.
    materials_path : str
        Path to materials CSV.
    po_path : str
        Path to purchase orders CSV.

    Returns
    -------
    dict
        The newly created purchase order record.
    """
    vendors_df = load_csv(vendors_path)
    materials_df = load_csv(materials_path)
    po_df = load_csv(po_path)

    vendor_row = vendors_df[vendors_df["vendor_number"] == vendor_number]
    if vendor_row.empty:
        raise ValueError(f"Vendor '{vendor_number}' not found.")

    material_row = materials_df[materials_df["material_number"] == material_number]
    if material_row.empty:
        raise ValueError(f"Material '{material_number}' not found.")

    vendor = vendor_row.iloc[0]
    material = material_row.iloc[0]

    if net_price is None:
        net_price = float(material["price"])

    new_id = int(po_df["po_id"].max()) + 1 if not po_df.empty else 1
    po_number = f"PO-{30000 + new_id:05d}"
    delivery_date = (date.today() + timedelta(days=delivery_days)).isoformat()

    new_record = {
        "po_id": new_id,
        "po_number": po_number,
        "po_date": date.today().isoformat(),
        "vendor_id": int(vendor["vendor_id"]),
        "vendor_number": vendor_number,
        "material_id": int(material["material_id"]),
        "material_number": material_number,
        "quantity": quantity,
        "unit_of_measure": material["unit_of_measure"],
        "net_price": net_price,
        "currency": currency,
        "delivery_date": delivery_date,
        "plant": plant,
        "storage_location": storage_location,
        "status": "OPEN",
        "gr_quantity": 0.0,
        "gr_date": "",
        "invoice_status": "PENDING",
    }

    po_df = pd.concat([po_df, pd.DataFrame([new_record])], ignore_index=True)
    save_purchase_orders(po_df, po_path)
    print(f"[ME21N] Purchase Order '{po_number}' created for vendor '{vendor_number}'.")
    return new_record


if __name__ == "__main__":
    record = create_purchase_order(
        vendor_number="VND-20001",
        material_number="MAT-10001",
        quantity=400.0,
        delivery_days=21,
    )
    print(record)
