"""
abc_analysis.py
Performs ABC classification of materials based on annual consumption value.
Class A: top 80% of cumulative value
Class B: next 15% (80-95%)
Class C: remaining 5% (95-100%)
"""

import pandas as pd
import os

DATA_PATH_INVENTORY = os.path.join(
    os.path.dirname(__file__), "..", "data", "inventory.csv"
)
DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)


def load_data(
    inventory_path: str = DATA_PATH_INVENTORY,
    materials_path: str = DATA_PATH_MATERIALS,
) -> pd.DataFrame:
    """Merge inventory and materials data for analysis."""
    inv_df = pd.read_csv(inventory_path)
    mat_df = pd.read_csv(materials_path)[
        ["material_id", "description", "material_type", "material_group"]
    ]
    return inv_df.merge(mat_df, on="material_id", how="left")


def run_abc_analysis(
    inventory_path: str = DATA_PATH_INVENTORY,
    materials_path: str = DATA_PATH_MATERIALS,
    class_a_threshold: float = 0.80,
    class_b_threshold: float = 0.95,
) -> pd.DataFrame:
    """
    Run ABC analysis on inventory data.

    Parameters
    ----------
    inventory_path : str
        Path to the inventory CSV.
    materials_path : str
        Path to the materials CSV.
    class_a_threshold : float
        Cumulative value % threshold for Class A (default 80%).
    class_b_threshold : float
        Cumulative value % threshold for Class B (default 95%).

    Returns
    -------
    pd.DataFrame
        DataFrame with ABC class assigned to each material.
    """
    df = load_data(inventory_path, materials_path)
    df = df.copy()
    df["annual_value"] = df["unrestricted_stock"] * df["valuation_price"]

    df = df.sort_values("annual_value", ascending=False).reset_index(drop=True)
    total_value = df["annual_value"].sum()

    if total_value == 0:
        df["abc_class"] = "C"
        return df

    df["cumulative_value"] = df["annual_value"].cumsum()
    df["cumulative_pct"] = df["cumulative_value"] / total_value

    def classify(cum_pct: float) -> str:
        if cum_pct <= class_a_threshold:
            return "A"
        elif cum_pct <= class_b_threshold:
            return "B"
        return "C"

    df["abc_class"] = df["cumulative_pct"].apply(classify)

    result = df[
        [
            "material_number",
            "description",
            "plant",
            "storage_location",
            "unrestricted_stock",
            "unit_of_measure",
            "valuation_price",
            "annual_value",
            "cumulative_pct",
            "abc_class",
        ]
    ]
    return result


def summary_by_class(abc_df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary table grouped by ABC class."""
    summary = (
        abc_df.groupby("abc_class")
        .agg(
            material_count=("material_number", "count"),
            total_value=("annual_value", "sum"),
        )
        .reset_index()
    )
    grand_total = summary["total_value"].sum()
    summary["value_pct"] = (summary["total_value"] / grand_total * 100).round(2)
    return summary


if __name__ == "__main__":
    result = run_abc_analysis()
    print("\n=== ABC Analysis Results ===")
    print(result.to_string(index=False))

    summary = summary_by_class(result)
    print("\n=== Summary by ABC Class ===")
    print(summary.to_string(index=False))
