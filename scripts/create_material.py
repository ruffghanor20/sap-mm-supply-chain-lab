"""
create_material.py
Simulates the SAP MM transaction MM01 - Create Material Master.
"""

import pandas as pd
import os
from datetime import date

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "materials.csv")


def load_materials(path: str = DATA_PATH) -> pd.DataFrame:
    """Load the materials CSV into a DataFrame."""
    return pd.read_csv(path)


def save_materials(df: pd.DataFrame, path: str = DATA_PATH) -> None:
    """Persist the DataFrame back to the materials CSV."""
    df.to_csv(path, index=False)


def material_exists(df: pd.DataFrame, material_number: str) -> bool:
    """Return True if a material with the given number already exists."""
    return material_number in df["material_number"].values


def create_material(
    material_number: str,
    description: str,
    material_type: str,
    material_group: str,
    unit_of_measure: str,
    price: float,
    currency: str = "USD",
    plant: str = "PL01",
    storage_location: str = "SL01",
    path: str = DATA_PATH,
) -> dict:
    """
    Create a new material master record.

    Parameters
    ----------
    material_number : str
        Unique material number (e.g. MAT-10011).
    description : str
        Short description of the material.
    material_type : str
        SAP material type (e.g. ROH, HIBE, NORM).
    material_group : str
        Material group code (e.g. MG001).
    unit_of_measure : str
        Base unit of measure (e.g. KG, PC, M, L).
    price : float
        Standard/moving average price per UoM.
    currency : str
        Currency code, default 'USD'.
    plant : str
        Plant code, default 'PL01'.
    storage_location : str
        Storage location, default 'SL01'.
    path : str
        Path to the materials CSV file.

    Returns
    -------
    dict
        The newly created material record.
    """
    df = load_materials(path)

    if material_exists(df, material_number):
        raise ValueError(f"Material '{material_number}' already exists.")

    new_id = int(df["material_id"].max()) + 1 if not df.empty else 1
    new_record = {
        "material_id": new_id,
        "material_number": material_number,
        "description": description,
        "material_type": material_type,
        "material_group": material_group,
        "unit_of_measure": unit_of_measure,
        "price": price,
        "currency": currency,
        "plant": plant,
        "storage_location": storage_location,
        "created_on": date.today().isoformat(),
    }

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    save_materials(df, path)
    print(f"[MM01] Material '{material_number}' created successfully (ID={new_id}).")
    return new_record


if __name__ == "__main__":
    record = create_material(
        material_number="MAT-10011",
        description="Stainless Steel Rod 20mm",
        material_type="ROH",
        material_group="MG001",
        unit_of_measure="KG",
        price=25.00,
    )
    print(record)
