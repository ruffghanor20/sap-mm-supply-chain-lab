"""
purchase_requisition.py
Simulates SAP MM transaction ME51N - Create Purchase Requisition.
"""

import pandas as pd
import os
from datetime import date, timedelta

DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)
PR_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "purchase_requisitions.csv"
)


def load_materials(path: str = DATA_PATH_MATERIALS) -> pd.DataFrame:
    """Load materials master data."""
    return pd.read_csv(path)


def load_requisitions(path: str = PR_OUTPUT_PATH) -> pd.DataFrame:
    """Load existing purchase requisitions or return empty DataFrame."""
    if os.path.exists(path):
        return pd.read_csv(path)
    columns = [
        "pr_id",
        "pr_number",
        "pr_date",
        "material_id",
        "material_number",
        "description",
        "quantity",
        "unit_of_measure",
        "required_date",
        "plant",
        "storage_location",
        "requested_by",
        "status",
    ]
    return pd.DataFrame(columns=columns)


def save_requisitions(df: pd.DataFrame, path: str = PR_OUTPUT_PATH) -> None:
    """Persist requisitions to CSV."""
    df.to_csv(path, index=False)


def create_purchase_requisition(
    material_number: str,
    quantity: float,
    required_date: str = None,
    plant: str = "PL01",
    storage_location: str = "SL01",
    requested_by: str = "SYSTEM",
    materials_path: str = DATA_PATH_MATERIALS,
    pr_path: str = PR_OUTPUT_PATH,
) -> dict:
    """
    Create a purchase requisition for a given material.

    Parameters
    ----------
    material_number : str
        Material number to requisition.
    quantity : float
        Required quantity.
    required_date : str
        ISO date string for when the material is needed (default: 30 days from today).
    plant : str
        Plant code.
    storage_location : str
        Storage location.
    requested_by : str
        User or department requesting the material.
    materials_path : str
        Path to materials CSV.
    pr_path : str
        Path to purchase requisitions CSV.

    Returns
    -------
    dict
        The newly created purchase requisition record.
    """
    materials_df = load_materials(materials_path)
    material_row = materials_df[materials_df["material_number"] == material_number]

    if material_row.empty:
        raise ValueError(f"Material '{material_number}' not found in master data.")

    material = material_row.iloc[0]
    pr_df = load_requisitions(pr_path)

    new_id = int(pr_df["pr_id"].max()) + 1 if not pr_df.empty else 1
    pr_number = f"PR-{40000 + new_id:05d}"

    if required_date is None:
        required_date = (date.today() + timedelta(days=30)).isoformat()

    new_record = {
        "pr_id": new_id,
        "pr_number": pr_number,
        "pr_date": date.today().isoformat(),
        "material_id": int(material["material_id"]),
        "material_number": material_number,
        "description": material["description"],
        "quantity": quantity,
        "unit_of_measure": material["unit_of_measure"],
        "required_date": required_date,
        "plant": plant,
        "storage_location": storage_location,
        "requested_by": requested_by,
        "status": "OPEN",
    }

    pr_df = pd.concat([pr_df, pd.DataFrame([new_record])], ignore_index=True)
    save_requisitions(pr_df, pr_path)
    print(f"[ME51N] Purchase Requisition '{pr_number}' created for '{material_number}'.")
    return new_record


if __name__ == "__main__":
    record = create_purchase_requisition(
        material_number="MAT-10001",
        quantity=300.0,
        requested_by="DEPT-PRODUCTION",
    )
    print(record)
