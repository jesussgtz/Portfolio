import pandas as pd

pd.set_option("display.width", 120)

DATA = "../data"

orders = pd.read_csv(f"{DATA}/olist_orders_dataset.csv", parse_dates=[
    "order_purchase_timestamp", "order_approved_at",
    "order_delivered_carrier_date", "order_delivered_customer_date",
    "order_estimated_delivery_date"
])
reviews = pd.read_csv(f"{DATA}/olist_order_reviews_dataset.csv")
items = pd.read_csv(f"{DATA}/olist_order_items_dataset.csv")
products = pd.read_csv(f"{DATA}/olist_products_dataset.csv")
customers = pd.read_csv(f"{DATA}/olist_customers_dataset.csv")
cat_translation = pd.read_csv(f"{DATA}/product_category_name_translation.csv")

print("=== SHAPES ===")
for name, df in [("orders", orders), ("reviews", reviews), ("items", items),
                  ("products", products), ("customers", customers)]:
    print(f"{name}: {df.shape}")

print("\n=== ORDERS: order_status counts ===")
print(orders["order_status"].value_counts())

print("\n=== ORDERS: date range ===")
print("purchase min/max:", orders["order_purchase_timestamp"].min(), orders["order_purchase_timestamp"].max())

print("\n=== ORDERS: null counts (key date columns) ===")
print(orders[["order_delivered_customer_date", "order_estimated_delivery_date",
              "order_approved_at", "order_delivered_carrier_date"]].isnull().sum())

# focus on delivered orders only, since delay only makes sense there
delivered = orders[orders["order_status"] == "delivered"].copy()
print(f"\nDelivered orders: {len(delivered)} / {len(orders)} total "
      f"({len(delivered)/len(orders):.1%})")

missing_delivered_date = delivered["order_delivered_customer_date"].isnull().sum()
print(f"Delivered orders missing delivered_customer_date: {missing_delivered_date}")

print("\n=== REVIEWS: review_score distribution ===")
print(reviews["review_score"].value_counts().sort_index())
print("Null review_score:", reviews["review_score"].isnull().sum())

print("\n=== REVIEWS: duplicate order_id? (should be ~1 review per order) ===")
print("total reviews:", len(reviews), " distinct order_id:", reviews["order_id"].nunique())

print("\n=== PRODUCTS: null product_category_name ===")
print(products["product_category_name"].isnull().sum(), "/", len(products))

print("\n=== PRODUCTS: distinct categories ===", products["product_category_name"].nunique())

print("\n=== CATEGORY TRANSLATION: rows ===", len(cat_translation))

print("\n=== ITEMS: rows per order (multi-item orders?) ===")
items_per_order = items.groupby("order_id").size()
print(items_per_order.describe())
