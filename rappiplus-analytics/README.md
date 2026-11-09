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

| Event | Unique users | Share of first-visit users |
|-------|--------------|---------------------------|
| first_visit | 7,796 | 100.00% |
| select_item | 7,582 | 97.26% |
| add_to_cart | 7,634 | 97.92% |
| begin_checkout | 7,208 | 92.46% |
| add_payment_info | 6,250 | 80.17% |
| purchase | 6,240 | 80.04% |

> **Interpretation note:** The SQL counts distinct users independently for each event and divides by first-visit users. It does not verify that events occurred in sequence for each user; the `add_to_cart` count even exceeds `select_item`. Treat these as event-reach rates, not a strict sequential funnel. The largest adjacent count decrease is between `begin_checkout` and `add_payment_info` (7,208 to 6,250), which is a useful area to investigate, not proof of payment-step causation.

### Step 4 — Cohort Retention (SQL · Window Functions)
Analyzed weekly cohort retention across 6 months using SQL window functions and visualized results as a heatmap.

> **Notebook interpretation:** Retention is described as remaining between 40–44% across cohorts and weeks 1–3. The notebook recommends early reactivation strategies for users who do not return in the first week.

### Step 5 — A/B Test (Python · statsmodels)
Tested whether a new checkout UI improved purchase conversion on a 10,000-user experiment (50/50 split).

| Group | Users | Conversions | Rate |
|-------|-------|-------------|------|
| Control | 4,965 | 779 | 15.69% |
| Treatment | 5,035 | 820 | 16.29% |

- **Absolute difference:** +0.60 percentage points (treatment minus control)
- **Z-statistic:** -0.8133
- **p-value:** 0.4161 (two-sided)
- **Significance level:** 0.05
- **Result:** Fail to reject H₀. The observed +0.60 pp difference is not statistically significant; the experiment does not provide sufficient evidence that the UI change improved conversion.

### Step 6 — Executive Dashboard (Power BI)
Built a 2-page Power BI dashboard with DAX measures, KPI cards, funnel chart, and cohort retention heatmap.

---

## Tools

`Python` · `pandas` · `NumPy` · `matplotlib` · `statsmodels` · `SQL` · `PostgreSQL` · `CTEs` · `Window Functions` · `Power BI` · `DAX` · `Jupyter Notebook`

---

## Files

- [`S12_RappiPlus_Clean.ipynb`](./S12_RappiPlus_Clean.ipynb) — Full analysis notebook (Steps 1–5)
