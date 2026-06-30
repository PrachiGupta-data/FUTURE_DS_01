# 📊 Superstore Sales Analysis — Business Performance Dashboard

A complete sales analytics project on 4 years (2014–2017) of retail order
data: cleaning, KPI analysis, trend/region/product breakdowns, and a
client-ready Excel dashboard with actionable recommendations.

> Built as part of the **Future Interns** Data Analytics task.
> Follow [Future Interns on LinkedIn](https://www.linkedin.com/company/future-interns/).

---

## 🎯 Problem

A retail superstore needed to understand: where is revenue actually growing,
which products and categories are profitable vs. quietly losing money, and
which regions need attention — using only their raw order-level export.

## 🔑 Key Findings

- **Revenue grew every year**, 2014→2017 (+51%), with profit growing even
  faster (+89%) — the business is healthy at the top line.
- **Discounting above 20% is unprofitable in aggregate.** Every discount band
  from 21–80% loses money; the cutoff is sharp, not gradual. Loss-making
  orders carry a 48% average discount vs. 8% on profitable ones.
- **Furniture (specifically Tables) is the structural problem**, not weak
  individual products. Tables loses -$17.7K overall because 55% of its orders
  get discounted 30%+, vs. 14% company-wide.
- **Central region underperforms on margin** (7.9%) despite mid-pack revenue
  — the same discounting issue shows up regionally.
- Revenue is sharply **seasonal**, spiking every November–December across all
  four years — a reliable planning signal.

Full writeup with all charts and the reasoning behind each recommendation:
**[ANALYSIS_REPORT.md](./ANALYSIS_REPORT.md)**

## 🛠️ Tools & Approach

- **Python** (pandas) — data cleaning, validation, aggregation
- **matplotlib** — chart generation
- **Excel / openpyxl** — final dashboard with live formulas (not hardcoded
  values) and native embedded charts across 6 sheets
- Data source: the public **Sample Superstore** dataset

## 📁 Repository Structure

```
├── ANALYSIS_REPORT.md              # Full written analysis & recommendations
├── Superstore_Sales_Dashboard.xlsx # Client-ready dashboard (6 sheets, live formulas)
├── clean_postal_codes.py           # Data cleaning fix script
├── generate_charts.py              # Chart generation script
├── data/
│   └── cleaned_superstore.csv      # Final cleaned dataset
└── assets/                         # Chart images (used in report + dashboard)
```

## 📈 Dashboard Preview

| Revenue Trend | Discount Impact on Profit |
|---|---|
| ![trend](assets/01_monthly_revenue_trend.png) | ![discount](assets/08_profit_by_discount_band.png) |

The full Excel workbook (`Superstore_Sales_Dashboard.xlsx`) includes:

1. **Executive Summary** — top-line KPIs and 6 key insights
2. **Revenue Trends** — monthly revenue/profit with native line chart
3. **Product & Category** — top 10 best/worst products, category breakdown
4. **Regional Performance** — region and sub-category profit comparison
5. **Discount Impact** — the discount-band-vs-profit analysis
6. **Raw Data** — full cleaned dataset (9,994 rows)

All KPIs are calculated with live Excel formulas referencing the Raw Data
sheet, so the dashboard updates automatically if the underlying data changes.

## 🧹 Data Cleaning Notes

The raw export had no duplicates, no missing values, and no invalid
sales/discount/quantity values — but postal codes were stored as integers,
which silently dropped leading zeros on 449 ZIP codes (e.g. `07090` →
`7090`). This is fixed in `clean_postal_codes.py`. A `Delivery Time` field
(days between order and ship date) was also engineered and validated against
an independent recalculation.

## 🚀 How to Reproduce

```bash
pip install pandas matplotlib openpyxl
python clean_postal_codes.py     # produces the cleaned dataset
python generate_charts.py        # produces all chart images
```

---

*This project was completed as part of the Future Interns Data Analytics
internship track.*
