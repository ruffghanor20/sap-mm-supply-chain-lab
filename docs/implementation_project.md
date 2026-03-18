# SAP MM Supply Chain Lab – Implementation Project

## Project Overview

This project simulates core SAP Materials Management (MM) processes using Python, CSV-based data storage, and analytics scripts. The goal is to provide a practical, hands-on lab environment for learning SAP MM concepts without requiring an SAP system.

---

## Project Scope

| Area | Description |
|---|---|
| Material Master | Create and manage material master records |
| Procurement | Purchase requisitions and purchase orders |
| Goods Receipt | Record inventory receipts against POs |
| Inventory Reporting | Stock overview and low-stock alerts |
| Analytics | ABC analysis, stock turnover, demand forecasting |

---

## Project Structure

```
sap-mm-supply-chain-lab/
│
├── README.md                    # Project overview
├── requirements.txt             # Python dependencies
│
├── data/                        # Simulated SAP master and transactional data
│   ├── materials.csv            # Material master (MM60)
│   ├── vendors.csv              # Vendor master (XK01)
│   ├── inventory.csv            # Stock data (MMBE / MB52)
│   └── purchase_orders.csv      # Purchase order data (ME21N)
│
├── scripts/                     # SAP MM process simulations
│   ├── create_material.py       # MM01 – Create Material Master
│   ├── purchase_requisition.py  # ME51N – Create Purchase Requisition
│   ├── create_purchase_order.py # ME21N – Create Purchase Order
│   ├── goods_receipt.py         # MIGO – Post Goods Receipt
│   └── inventory_report.py      # MB52 / MMBE – Inventory Reports
│
├── analytics/                   # Supply chain analytics
│   ├── abc_analysis.py          # ABC inventory classification
│   ├── stock_turnover.py        # Turnover ratio and days-on-hand
│   └── demand_forecast.py       # SMA and exponential smoothing forecast
│
├── dashboard/                   # Business intelligence
│   └── powerbi_model.pbix       # Power BI dashboard model (placeholder)
│
└── docs/                        # Documentation
    ├── sap_mm_process.md        # SAP MM process descriptions
    └── implementation_project.md # This document
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Data Processing | pandas, numpy |
| Forecasting | statsmodels, scikit-learn |
| Visualization | matplotlib, seaborn |
| BI Dashboard | Microsoft Power BI |
| Data Storage | CSV files (simulating SAP tables) |
| Testing | pytest |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ruffghanor20/sap-mm-supply-chain-lab.git
cd sap-mm-supply-chain-lab
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage Examples

### Create a new material master
```bash
python scripts/create_material.py
```

### Create a purchase requisition
```bash
python scripts/purchase_requisition.py
```

### Create a purchase order
```bash
python scripts/create_purchase_order.py
```

### Post a goods receipt
```bash
python scripts/goods_receipt.py
```

### Generate inventory report
```bash
python scripts/inventory_report.py
```

### Run ABC analysis
```bash
python analytics/abc_analysis.py
```

### Calculate stock turnover
```bash
python analytics/stock_turnover.py
```

### Generate demand forecast
```bash
python analytics/demand_forecast.py
```

---

## SAP MM Data Model (Simulated)

### Materials Table (`data/materials.csv`)
Corresponds to SAP table `MARA` (General Material Data) and `MARC` (Plant Data).

| Field | SAP Equivalent | Description |
|---|---|---|
| material_id | MATNR (internal) | Unique identifier |
| material_number | MATNR | Material number |
| description | MAKTX | Short description |
| material_type | MTART | Material type (ROH, HIBE, etc.) |
| material_group | MATKL | Material group |
| unit_of_measure | MEINS | Base unit of measure |
| price | STPRS / VERPR | Standard / moving average price |

### Vendors Table (`data/vendors.csv`)
Corresponds to SAP table `LFA1` (Vendor Master General Section).

### Inventory Table (`data/inventory.csv`)
Corresponds to SAP table `MARD` (Storage Location Data for Material).

### Purchase Orders Table (`data/purchase_orders.csv`)
Corresponds to SAP tables `EKKO` (PO Header) and `EKPO` (PO Item).

---

## Project Milestones

| Phase | Description | Status |
|---|---|---|
| 1 | Repository setup and data model | ✅ Complete |
| 2 | Core MM process scripts | ✅ Complete |
| 3 | Inventory analytics | ✅ Complete |
| 4 | Demand forecasting | ✅ Complete |
| 5 | Power BI dashboard | 🔄 In Progress |
| 6 | Documentation | ✅ Complete |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
