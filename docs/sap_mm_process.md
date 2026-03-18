# SAP MM Process Documentation

## Overview

SAP Materials Management (MM) is a core module of SAP ERP that handles all procurement and inventory management processes. This document describes the key MM processes simulated in this lab.

---

## 1. Material Master (MM01 / MM02 / MM03)

The **Material Master** is the central repository of information that a company maintains for each material it uses.

### Key Organizational Levels
| Level | Description |
|---|---|
| Client | Highest level; data valid for entire company |
| Plant | Production unit or branch |
| Storage Location | Physical location within a plant |
| Purchasing Organization | Entity responsible for procurement |

### Material Types
| Code | Description |
|---|---|
| ROH | Raw Material |
| HIBE | Operating Supplies |
| NORM | Standard Part |
| FERT | Finished Product |
| HALB | Semi-Finished Product |

### Process Flow
```
MM01 (Create) → MM02 (Change) → MM03 (Display) → MM60 (Inventory Turnover)
```

---

## 2. Purchase Requisition (ME51N / ME52N / ME53N)

A **Purchase Requisition (PR)** is an internal document that requests the Purchasing department to procure a specific quantity of material by a required date.

### PR Status Values
| Status | Description |
|---|---|
| OPEN | Requisition created, awaiting PO |
| IN_PROCESS | Being converted to a Purchase Order |
| CLOSED | Fully covered by a Purchase Order |

### Key Fields
- **Material Number** – Identifies the material to be procured
- **Quantity** – Required quantity in base unit of measure
- **Required Date** – Date by which the material is needed
- **Plant / Storage Location** – Where material should be delivered
- **Requested By** – Requesting department or user

---

## 3. Purchase Order (ME21N / ME22N / ME23N)

A **Purchase Order (PO)** is a formal document sent to a vendor requesting the supply of materials or services.

### PO Types
| Type | Description |
|---|---|
| Standard PO | One-time order for materials |
| Blanket PO | Framework agreement for recurring orders |
| Subcontracting PO | Vendor uses company-supplied components |
| Stock Transfer | Transfer between plants |

### PO Status Values
| Status | Description |
|---|---|
| OPEN | PO created, no GR posted |
| GR_DONE | Partial or full goods receipt posted |
| COMPLETED | Fully received and invoiced |

---

## 4. Goods Receipt (MIGO - Movement Type 101)

**Goods Receipt (GR)** is the process of recording the arrival of materials at the plant/warehouse.

### Effects of Goods Receipt
1. **Inventory increase** – Unrestricted stock is updated
2. **Accounting document** – GR/IR clearing account is credited
3. **PO history update** – GR quantity and date recorded on the PO

### Movement Types
| Type | Description |
|---|---|
| 101 | GR for Purchase Order |
| 201 | GI for Cost Center |
| 261 | GI for Production Order |
| 301 | Transfer Posting between Plants |

---

## 5. Invoice Verification (MIRO)

**Invoice Verification** matches the vendor invoice against the Purchase Order and Goods Receipt (3-way match).

### 3-Way Match
```
Purchase Order ↔ Goods Receipt ↔ Vendor Invoice
```

### Tolerances
Small differences in price or quantity between PO, GR, and invoice may be accepted within defined tolerance limits.

---

## 6. Inventory Management (MB52 / MMBE)

### Key Reports
| Transaction | Description |
|---|---|
| MB52 | Warehouse stocks of material |
| MMBE | Stock overview |
| MB51 | Material document list |
| MB5B | Stocks for posting date |

### Stock Categories
| Category | Description |
|---|---|
| Unrestricted | Available for use/sale |
| Quality Inspection | Under QC review |
| Blocked | Not available for use |
| In Transit | Being transferred |

---

## 7. ABC Analysis

ABC analysis classifies materials based on their consumption value:

| Class | Cumulative Value | Focus |
|---|---|---|
| A | Top 80% | High attention, tight control |
| B | 80–95% | Medium control |
| C | Bottom 5% | Minimal control, bulk ordering |

---

## References
- SAP Help Portal: https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/material-management
- SAP MM Configuration Guide
- APICS Supply Chain Management Fundamentals
