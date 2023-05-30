import pandas as pd
import json
import matplotlib.pyplot as plt
from utils.utils import cancellation_rate, calculate_lifetime_value

HARDWARE_DATA_PATH = "data/hardware_sales.xlsx"
CUSTOMER_DATA_PATH = "data/customers.csv"
SUBSCRIPTION_EVENTS_DATA_PATH = "data/subscription_events.json"

json_data = []
orders_data = {}
# hardware_sales = []
cancelled_subscriptions = []

# EXTRACT ------------------------------------------------------------------
hardware_sales_df = pd.read_excel(HARDWARE_DATA_PATH)
customer_df = pd.read_csv(CUSTOMER_DATA_PATH)
print(customer_df)

with open(SUBSCRIPTION_EVENTS_DATA_PATH, 'r') as subscription_events_file:
    for json_object in subscription_events_file:
        json_parsed = json.loads(json_object)

        event_type = json_parsed.get("event_type")
        order_id = json_parsed.get("order_id")

        if event_type == "subscription_created":
            orders_data[order_id] = {
                "customer_id": json_parsed["customer_id"],
                "revenue": json_parsed["revenue"]
            }
        else:
            related_data = orders_data.get(order_id)

            if event_type == "subscription_cancelled":
                cancelled_subscriptions.append(order_id)

            if related_data:
                json_parsed["customer_id"] = related_data.get("customer_id")
                json_parsed["revenue"] = related_data.get("revenue")

        json_data.append(json_parsed)

# TRANSFORM ------------------------------------------------------------------
subscription_events_df = pd.DataFrame(data=json_data)

cancellation_rate = cancellation_rate(subscription_events_df, cancelled_subscriptions)

calculate_lifetime_value(subscription_events_df)
# Hardware Events
hardware_revenue = hardware_sales_df["revenue"].sum()

# Subscription Created
df_filtered_created = subscription_events_df[subscription_events_df["event_type"] == "subscription_created"]
total_created_revenue = df_filtered_created["revenue"].sum()
# cumulative_total_created_revenue = df_filtered_created["revenue"].cumsum().plot()

# Subscription Renewed
df_filtered_renewed = subscription_events_df[subscription_events_df["event_type"] == "subscription_renewed"]
total_renewed_revenue = df_filtered_renewed["revenue"].sum()
# cumulative_total_renewed_revenue = df_filtered_renewed["revenue"].cumsum().plot()

# Subscription Cancelled
df_filtered_cancelled = subscription_events_df[subscription_events_df["event_type"] == "subscription_cancelled"]
total_cancelled_revenue = df_filtered_cancelled["revenue"].sum()
# cumulative_total_cancelled_revenue = df_filtered_cancelled["revenue"].cumsum().plot()

# LOAD ------------------------------------------------------------------
plt.bar(['Created', 'Renewed', 'Hardware'], [total_created_revenue, total_renewed_revenue, hardware_revenue])
plt.xlabel('Event Type')
plt.ylabel('Revenue')
plt.title('Revenue to date')
plt.show()

cumulative_total_created_revenue = df_filtered_created["revenue"].cumsum().plot()
cumulative_total_renewed_revenue = df_filtered_renewed["revenue"].cumsum().plot()
cumulative_total_cancelled_revenue = df_filtered_cancelled["revenue"].cumsum().plot()
plt.show()