import pandas as pd
from utils.utils import cancellation_rate, calculate_lifetime_value, plot_cumulative_sum, plot_revenue_sum, parse_event_json

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

json_data, orders_data, cancelled_subscriptions = parse_event_json(json_file=SUBSCRIPTION_EVENTS_DATA_PATH)

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

# PLOT ------------------------------------------------------------------
plot_revenue_sum(total_created_revenue, total_renewed_revenue, hardware_revenue)
plot_cumulative_sum(df_filtered_created, df_filtered_renewed, df_filtered_cancelled)