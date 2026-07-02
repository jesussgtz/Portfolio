# RappiPlus Business Analytics

End-to-end business analytics project for a subscription e-commerce platform. The goal was to evaluate the performance of RappiPlus and generate data-driven recommendations to support business decisions.

---

## Business Context

RappiPlus is a subscription-based e-commerce service operating across Latin America. This analysis covers 6 months of transactional data (Jan–Jun 2025) across three countries and multiple product categories.

**Business questions answered:**
- Is the business profitable?
- Where are users dropping off in the purchase funnel?
- Are users coming back after their first purchase?
- Did a checkout UI change improve conversion?

---

## Datasets

| File | Description |
|------|-------------|
| `rappiplus_orders_raw.csv` | 25,100 order records with pricing, discounts, and revenue |
| `rappiplus_catalog.csv` | Product costs and categories |
| `rappiplus_marketing_spend.csv` | Marketing investment by channel and country |
| `events` / `users` / `user_activity` (SQL) | User behavior on the platform |
| `experiment_checkout_ui.csv` | A/B test results for checkout UI change |

---

## Analysis

### Step 1 — Data Quality
- Removed 100 duplicates from 25,100 orders
- Handled nulls in country, device, and product columns
- Fixed encoding inconsistencies in product categories
- Removed 4 rows with negative `monto_total`
- **Final dataset: 24,946 clean orders**

### Step 2 — Business Profitability (Python)
- Calculated Revenue, COGS, and Marketing Spend
- Computed Profit and margin
- Analyzed top-selling products and marketing channel spend

| KPI | Value |
|-----|-------|
| Revenue | $51.97M |
| COGS | $43.12M |
| Marketing Investment | $2.87M |
| **Profit** | **$5.97M** |
| **Profit Margin** | **11.5%** |
| Avg. Order Value | $2,083 |

### Step 3 — Conversion Funnel (SQL · PostgreSQL)
Built a 6-step funnel using CTEs to track users from session start to purchase.

| Step | Users | Conversion |
|------|-------|------------|
| view_item | 7,796 | — |
| add_to_cart | 7,492 | 96% |
| begin_checkout | 7,148 | 95% |
| add_payment_info | 6,598 | **92%** |
| purchase | 5,268 | **80%** ⚠️ |

> **Key finding:** The biggest drop-off happens at `add_payment_info → purchase` (92% → 80%). Optimizing the payment step could significantly increase conversion.

### Step 4 — Cohort Retention (SQL · Window Functions)
Analyzed weekly cohort retention across 6 months using SQL window functions and visualized results as a heatmap.

> **Key finding:** Retention stabilizes between 30–40% after week 2, suggesting a loyal returning user base but significant first-week churn.

### Step 5 — A/B Test (Python · statsmodels)
Tested whether a new checkout UI improved purchase conversion on a 10,000-user experiment (50/50 split).

| Group | Users | Conversions | Rate |
|-------|-------|-------------|------|
| Control | 5,000 | ~2,100 | ~42% |
| Treatment | 5,000 | ~2,130 | ~42.6% |

- **Z-statistic:** -0.81
- **p-value:** 0.42
- **Result:** Fail to reject H₀ — no statistically significant difference. The UI change did not improve conversion.

### Step 6 — Executive Dashboard (Power BI)
Built a 2-page Power BI dashboard with DAX measures, KPI cards, funnel chart, and cohort retention heatmap.

---

## Tools

`Python` · `pandas` · `NumPy` · `matplotlib` · `statsmodels` · `SQL` · `PostgreSQL` · `CTEs` · `Window Functions` · `Power BI` · `DAX` · `Jupyter Notebook`

---

## Files

- [`S12_RappiPlus_Clean.ipynb`](./S12_RappiPlus_Clean.ipynb) — Full analysis notebook (Steps 1–5)
