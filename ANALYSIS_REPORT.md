# Superstore Sales Analysis — Report

**Period covered:** January 2014 – December 2017
**Records analyzed:** 9,994 orders
**Tools used:** Python (pandas, matplotlib), Excel (openpyxl, native formulas & charts)

---

## 1. Overview

This report analyzes four years of order-level sales data from a national retail
superstore (Sales, Furniture, Office Supplies, and Technology categories) to
identify revenue trends, top-performing and underperforming products, and
regional patterns, with the goal of producing recommendations a business owner
could act on directly.

**Headline numbers:**

| Metric | Value |
|---|---|
| Total Revenue | $2,297,201 |
| Total Profit | $286,397 |
| Overall Profit Margin | 12.5% |
| Total Orders | 9,994 |
| Orders Sold at a Loss | 1,871 (18.7%) |

---

## 2. Data Cleaning

The raw export (`Sample - Superstore.csv`) was checked for the standard set of
data-quality issues before analysis:

- **Duplicates:** none found (0 full-row duplicates).
- **Missing values:** none found across all 21 original columns.
- **Invalid values:** no negative or zero Sales, no zero/negative Quantity, all
  Discount values fall within a valid 0–80% range.
- **Postal codes stored as integers**, which silently strips leading zeros from
  ZIP codes in the northeastern US (e.g., `07090` → `7090`). This affected 449
  rows (4.5% of the dataset). Fixed by casting to a zero-padded 5-character
  string. This has no effect on the sales/profit analysis below, but matters
  for any downstream use of the data involving geography or mailing.
- **Feature engineering:** added a `Delivery Time` column (Ship Date − Order
  Date, in days) to support fulfillment-speed analysis. Verified against an
  independent recalculation — 0 mismatches across all 9,994 rows.

See `clean_postal_codes.py` for the fix and `data/cleaned_superstore.csv` for
the final cleaned dataset.

---

## 3. Revenue Trends Over Time

![Monthly Revenue Trend](assets/01_monthly_revenue_trend.png)

Revenue grew every year of the dataset:

| Year | Revenue | Profit |
|---|---|---|
| 2014 | $484,247 | $49,544 |
| 2015 | $470,533 | $61,619 |
| 2016 | $609,206 | $81,795 |
| 2017 | $733,215 | $93,439 |

Revenue is also strongly **seasonal**: every year shows a sharp spike in
November and December, consistent with holiday-season buying, followed by a
drop-off in January–February. This pattern is consistent enough across all
four years to be used for inventory and staffing planning, not just observed
as noise.

**Note:** 2015 revenue dipped slightly versus 2014 even though profit still
grew — this is consistent with the discounting pattern described in Section 6,
and is worth flagging rather than treating as a one-off anomaly.

---

## 4. Top-Selling Products

![Top 10 Products by Sales](assets/02_top10_products_by_sales.png)

The Canon imageCLASS 2200 Advanced Copier is the single largest revenue driver
in the dataset ($61,600), more than double the next closest product. The top
10 list is dominated by **Technology** items (copiers, binding systems,
videoconferencing equipment) — high-ticket, low-frequency purchases rather
than high-volume consumables.

---

## 5. Loss-Making Products

![Top 10 Loss-Making Products](assets/03_top10_loss_products.png)

Ten products account for a combined **-$29,400** in losses, led by the Cubify
CubeX 3D Printer (Double Head Print) at -$8,880. Several of these same
product *families* (Cubify CubeX, GBC DocuBind, Cisco TelePresence) appear in
both the top-seller and top-loss lists — meaning the issue is not lack of
demand, but margin: these products are being sold, just unprofitably.

---

## 6. Why Are These Products Losing Money? — Discount Impact

![Profit by Discount Band](assets/08_profit_by_discount_band.png)

This is the most important finding in the analysis. When orders are grouped
by discount level, there is a sharp, consistent cutoff:

| Discount Band | Total Profit |
|---|---|
| 0% | +$320,063 |
| 1–10% | +$8,496 |
| 11–20% | +$91,873 |
| 21–30% | **-$10,099** |
| 31–40% | **-$26,762** |
| 41–50% | **-$22,233** |
| 51–80% | **-$74,940** |

Every discount band above 20% loses money in aggregate. The average discount
on loss-making orders is **48%**, versus just **8.1%** on profitable orders.
This is not a demand or pricing-of-goods problem — it is a **discount policy**
problem.

The **Tables** sub-category is the clearest example: it loses -$17,725
overall, the single worst-performing sub-category in the dataset, and 55.2%
of its orders carry a discount of 30% or more (vs. 13.9% company-wide).

---

## 7. Category & Sub-Category Performance

![Profit by Category](assets/06_profit_by_category.png)
![Profit by Sub-Category](assets/07_profit_by_subcategory.png)

| Category | Sales | Profit | Margin |
|---|---|---|---|
| Technology | $836,154 | $145,455 | 17.4% |
| Office Supplies | $719,047 | $122,491 | 17.0% |
| Furniture | $741,999 | $18,451 | 2.5% |

Furniture generates nearly as much revenue as the other two categories but
converts almost none of it to profit. This is driven almost entirely by two
sub-categories: **Tables** (-$17,725) and **Bookcases** (-$3,473), both of
which sit inside Furniture.

---

## 8. Regional Performance

![Sales by Region](assets/04_sales_by_region.png)
![Profit by Region](assets/05_profit_by_region.png)

| Region | Sales | Profit | Margin |
|---|---|---|---|
| West | $725,458 | $108,418 | 14.9% |
| East | $678,781 | $91,523 | 13.5% |
| Central | $501,240 | $39,706 | 7.9% |
| South | $391,722 | $46,749 | 11.9% |

**Central** is the clear underperformer: it generates more revenue than South
but converts it to profit at roughly half the rate (7.9% vs. 11.9–14.9%
elsewhere). Given that discounting is the dominant driver of margin loss
company-wide, Central is the first region worth auditing for discount
practices.

---

## 9. Recommendations

1. **Cap discounts at 20% on Furniture, especially Tables**, or require
   manager approval above that threshold. The data shows a hard profitability
   cliff at this point, not a gradual decline — this is the single highest-
   leverage fix available in the dataset.
2. **Audit pricing on the Cubify CubeX 3D Printer and GBC DocuBind product
   lines.** These sell well but lose money on every unit; either renegotiate
   supplier cost, raise price, or reduce the discount allowed on them
   specifically.
3. **Investigate discount approval practices in the Central region.** It
   underperforms East and West on margin despite comparable revenue scale,
   and the company-wide pattern points to discounting as the likely cause.
4. **Plan inventory and staffing around the November–December demand spike**
   that appears consistently across all four years — this is a reliable,
   recurring pattern, not noise.
5. **Lean into what's working**: Technology and Office Supplies both convert
   sales to profit at ~17% margin. Marketing spend and floor space
   reallocated toward these categories, and away from underperforming
   Furniture sub-categories, would likely improve blended margin without
   needing to grow total revenue.

---

## 10. Files in This Repository

| File | Description |
|---|---|
| `Superstore_Sales_Dashboard.xlsx` | Client-ready Excel dashboard: Executive Summary, Revenue Trends, Product & Category, Regional Performance, Discount Impact, and full cleaned Raw Data — all KPIs and pivot tables are live formulas, not hardcoded values. |
| `data/cleaned_superstore.csv` | Final cleaned dataset (9,994 rows, postal codes fixed, delivery time added). |
| `clean_postal_codes.py` | Script fixing the postal-code leading-zero bug. |
| `generate_charts.py` | Script generating all charts in `assets/`. |
| `assets/` | All chart images used in this report and the dashboard. |
