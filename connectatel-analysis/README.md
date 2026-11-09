# ConnectaTel Customer Analysis

## Objective

Analyze customer behavior for a Latin American telecom provider to identify usage patterns, segment customers, detect data-quality issues, and suggest ways to improve plan fit.

## Data

The notebook loads three datasets:

| Dataset | Records / scope | Contents |
|---|---:|---|
| `users_latam.csv` | 4,000 users | Age, city, registration date, plan, churn date |
| `usage.csv` | 40,000 usage records | Calls, messages, dates, duration, message length |
| `plans.csv` | 2 plans | Included minutes/messages/data and extra-use prices |

The analysis uses 2024 usage records. The notebook also identifies 40 user registration dates in 2026 and marks dates beyond 2024 as invalid for this assignment.

## Analysis Process

1. Explored schemas, data types, missing values, sentinels, and date ranges.
2. Cleaned invalid age and city values and assessed missing usage fields.
3. Aggregated calls, messages, and call duration by user.
4. Compared usage distributions by plan and examined outliers with the IQR method.
5. Segmented customers by usage level and age group.

## Data Quality Findings

- `city`: 469 of 4,000 records (11.7%) were initially null; another 96 used the invalid `?` placeholder. Both were treated as missing, for 565 missing city values after cleanup (14.1%).
- `age`: the invalid sentinel `-999` was replaced with the median age (47).
- `churn_date`: all 4,000 values were missing, so churn could not be analyzed from this field.
- `duration` is missing for almost all text records, while `length` is missing for almost all call records. The notebook checks this relationship and retains these type-specific nulls rather than treating them as general data loss.
- 50 usage dates were missing; registration dates beyond 2024 were excluded from the assignment's analysis period.

## Usage and Segmentation

- Average customer age after cleaning: 48.1 years.
- 64.9% of users were on the Básico plan and 35.1% on Premium.
- Average recorded usage per user: 5.5 messages, 4.5 calls, and 23.3 call minutes.
- Usage groups are rule-based: Bajo uso (fewer than 5 calls and 5 messages), Uso medio (fewer than 10 calls and 10 messages, after excluding Bajo uso), and Alto uso (the remaining users).
- Age groups are Joven (under 30), Adulto (30–59), and Adulto Mayor (60+).
- The notebook's written executive summary identifies Uso medio as the largest usage segment. Exact segment counts are not printed in the saved notebook outputs.

## Outliers and Business Considerations

The notebook identifies high-end outliers in messages, calls, and especially call minutes, but keeps them because they may represent genuine intensive usage. These customers may warrant plan-fit analysis. High usage alone does not establish customer profitability or lifetime value; the notebook does not calculate either.

The notebook suggests considering an intermediate plan for medium-use customers, tailored options for high-use customers, and engagement strategies for low-use customers. These are recommendations to test, not measured revenue impacts.

## Tools

Python · pandas · NumPy · matplotlib · seaborn · Jupyter Notebook

## How to Run

Open the notebook in Google Colab or Jupyter Notebook and run the cells sequentially. The original notebook references the datasets at `/datasets/plans.csv`, `/datasets/users_latam.csv`, and `/datasets/usage.csv`; provide those files at the expected paths or update the paths before running.
