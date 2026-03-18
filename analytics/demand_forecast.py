"""
demand_forecast.py
Generates demand forecasts using simple moving average and exponential smoothing.
Uses historical purchase order data as a proxy for demand.
"""

import pandas as pd
import numpy as np
import os
from datetime import date, timedelta

DATA_PATH_PO = os.path.join(
    os.path.dirname(__file__), "..", "data", "purchase_orders.csv"
)
DATA_PATH_MATERIALS = os.path.join(
    os.path.dirname(__file__), "..", "data", "materials.csv"
)


def load_data(
    po_path: str = DATA_PATH_PO,
    materials_path: str = DATA_PATH_MATERIALS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load purchase orders and materials data."""
    po_df = pd.read_csv(po_path, parse_dates=["po_date"])
    mat_df = pd.read_csv(materials_path)
    return po_df, mat_df


def build_monthly_demand(
    material_number: str,
    po_path: str = DATA_PATH_PO,
    materials_path: str = DATA_PATH_MATERIALS,
) -> pd.Series:
    """
    Build a monthly demand series for a given material from PO history.

    Parameters
    ----------
    material_number : str
        The material number to build demand for.
    po_path : str
        Path to purchase orders CSV.
    materials_path : str
        Path to materials CSV.

    Returns
    -------
    pd.Series
        Monthly demand indexed by period (YYYY-MM).
    """
    po_df, _ = load_data(po_path, materials_path)
    mat_po = po_df[po_df["material_number"] == material_number].copy()

    if mat_po.empty:
        return pd.Series(dtype=float)

    mat_po["month"] = mat_po["po_date"].dt.to_period("M")
    monthly = mat_po.groupby("month")["quantity"].sum()
    return monthly


def moving_average_forecast(
    series: pd.Series,
    window: int = 3,
    forecast_periods: int = 3,
) -> pd.Series:
    """
    Simple Moving Average (SMA) forecast.

    Parameters
    ----------
    series : pd.Series
        Historical demand series.
    window : int
        Number of periods to use in the moving average.
    forecast_periods : int
        Number of future periods to forecast.

    Returns
    -------
    pd.Series
        Forecasted values for the next `forecast_periods` periods.
    """
    if len(series) < window:
        avg = series.mean() if not series.empty else 0.0
    else:
        avg = series.iloc[-window:].mean()

    last_period = series.index[-1] if not series.empty else pd.Period(date.today().strftime("%Y-%m"), "M")
    future_periods = [last_period + i for i in range(1, forecast_periods + 1)]
    return pd.Series([round(avg, 2)] * forecast_periods, index=future_periods)


def exponential_smoothing_forecast(
    series: pd.Series,
    alpha: float = 0.3,
    forecast_periods: int = 3,
) -> pd.Series:
    """
    Single Exponential Smoothing (SES) forecast.

    Parameters
    ----------
    series : pd.Series
        Historical demand series.
    alpha : float
        Smoothing factor (0 < alpha < 1). Higher = more weight on recent data.
    forecast_periods : int
        Number of future periods to forecast.

    Returns
    -------
    pd.Series
        Forecasted values for the next `forecast_periods` periods.
    """
    if series.empty:
        return pd.Series(dtype=float)

    smoothed = float(series.iloc[0])
    for value in series.iloc[1:]:
        smoothed = alpha * float(value) + (1 - alpha) * smoothed

    last_period = series.index[-1]
    future_periods = [last_period + i for i in range(1, forecast_periods + 1)]
    return pd.Series([round(smoothed, 2)] * forecast_periods, index=future_periods)


def forecast_all_materials(
    po_path: str = DATA_PATH_PO,
    materials_path: str = DATA_PATH_MATERIALS,
    window: int = 3,
    alpha: float = 0.3,
    forecast_periods: int = 3,
) -> pd.DataFrame:
    """
    Run demand forecast for all materials in the purchase order history.

    Returns
    -------
    pd.DataFrame
        Forecast results with SMA and SES predictions for each material.
    """
    po_df, mat_df = load_data(po_path, materials_path)
    material_numbers = po_df["material_number"].unique()

    rows = []
    for mat_num in material_numbers:
        series = build_monthly_demand(mat_num, po_path, materials_path)
        if series.empty:
            continue

        sma = moving_average_forecast(series, window=window, forecast_periods=forecast_periods)
        ses = exponential_smoothing_forecast(series, alpha=alpha, forecast_periods=forecast_periods)

        for i, period in enumerate(sma.index):
            rows.append(
                {
                    "material_number": mat_num,
                    "forecast_period": str(period),
                    "sma_forecast": sma.iloc[i],
                    "ses_forecast": ses.iloc[i],
                }
            )

    result = pd.DataFrame(rows)
    if not result.empty:
        mat_desc = mat_df[["material_number", "description", "unit_of_measure"]]
        result = result.merge(mat_desc, on="material_number", how="left")

    return result


if __name__ == "__main__":
    forecasts = forecast_all_materials(forecast_periods=3)
    print("\n=== Demand Forecast (Next 3 Months) ===")
    print(forecasts.to_string(index=False))
