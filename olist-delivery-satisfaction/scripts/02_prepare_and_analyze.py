import pandas as pd
import numpy as np

pd.set_option("display.width", 120)
DATA = "../data"
OUT = "../output"

orders = pd.read_csv(f"{DATA}/olist_orders_dataset.csv", parse_dates=[
    "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"
])
reviews = pd.read_csv(f"{DATA}/olist_order_reviews_dataset.csv", parse_dates=["review_creation_date"])
items = pd.read_csv(f"{DATA}/olist_order_items_dataset.csv")
products = pd.read_csv(f"{DATA}/olist_products_dataset.csv")
cat_translation = pd.read_csv(f"{DATA}/product_category_name_translation.csv")

# --- 1. Only delivered orders with a valid delivered date ---
delivered = orders[orders["order_status"] == "delivered"].copy()
delivered = delivered.dropna(subset=["order_delivered_customer_date", "order_estimated_delivery_date"])

# --- 2. Delivery delay in days (positive = late, negative = early) ---
delivered["delivery_delay_days"] = (
    delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# --- 3. Deduplicate reviews: keep the most recent review per order ---
reviews_dedup = (
    reviews.sort_values("review_creation_date")
    .drop_duplicates(subset="order_id", keep="last")[["order_id", "review_score"]]
)

# --- 4. One category per order: take the first item's product/category ---
items_first = items.sort_values(["order_id", "order_item_id"]).drop_duplicates(
    subset="order_id", keep="first"
)[["order_id", "product_id"]]

products_cat = products[["product_id", "product_category_name"]].merge(
    cat_translation, on="product_category_name", how="left"
)
products_cat["category_en"] = products_cat["product_category_name_english"].fillna(
    products_cat["product_category_name"]
).fillna("unknown")

order_category = items_first.merge(products_cat[["product_id", "category_en"]], on="product_id", how="left")
order_category["category_en"] = order_category["category_en"].fillna("unknown")

# --- 5. Merge everything at order grain ---
df = (
    delivered[["order_id", "delivery_delay_days"]]
    .merge(reviews_dedup, on="order_id", how="inner")
    .merge(order_category[["order_id", "category_en"]], on="order_id", how="left")
)
df["category_en"] = df["category_en"].fillna("unknown")

print("Final analysis table shape:", df.shape)
print(df.head())
df.to_csv(f"{OUT}/order_delay_review.csv", index=False)

# --- 6. Flag late vs on-time/early ---
df["is_late"] = df["delivery_delay_days"] > 0

print("\n=== Late vs on-time/early: counts ===")
print(df["is_late"].value_counts())
print("\n=== Average review_score: late vs on-time/early ===")
print(df.groupby("is_late")["review_score"].mean())

print("\n=== Correlation (delay_days vs review_score) ===")
print(df[["delivery_delay_days", "review_score"]].corr())

print("\n=== Average review_score by delay bucket ===")
bins = [-np.inf, -7, -1, 0, 3, 7, 15, np.inf]
labels = ["7+ dias antes", "1-7 dias antes", "a tiempo", "1-3 dias tarde",
          "4-7 dias tarde", "8-15 dias tarde", "15+ dias tarde"]
df["delay_bucket"] = pd.cut(df["delivery_delay_days"], bins=bins, labels=labels)
bucket_summary = df.groupby("delay_bucket", observed=True).agg(
    n_orders=("order_id", "count"), avg_review=("review_score", "mean")
)
print(bucket_summary)
bucket_summary.to_csv(f"{OUT}/delay_bucket_summary.csv")

print("\n=== Categories with biggest satisfaction drop when late (min 100 orders each side) ===")
cat_stats = df.groupby(["category_en", "is_late"])["review_score"].agg(["mean", "count"]).unstack()
cat_stats.columns = ["_".join(map(str, c)) for c in cat_stats.columns]
cat_stats = cat_stats.dropna(subset=["mean_False", "mean_True"])
cat_stats = cat_stats[(cat_stats["count_False"] >= 100) & (cat_stats["count_True"] >= 20)]
cat_stats["score_drop"] = cat_stats["mean_False"] - cat_stats["mean_True"]
cat_stats = cat_stats.sort_values("score_drop", ascending=False)
print(cat_stats.head(15))
cat_stats.to_csv(f"{OUT}/category_delay_impact.csv")
