import pandas as pd
from utils.utils import cancellation_rate, calculate_lifetime_value, plot_cumulative_sum, plot_revenue_sum, \
    parse_event_json, calculate_total_revenue_to_date

HARDWARE_DATA_PATH = "data/hardware_sales.xlsx"
CUSTOMER_DATA_PATH = "data/customers.csv"
SUBSCRIPTION_EVENTS_DATA_PATH = "data/subscription_events.json"

json_data = []
orders_data = {}
cancelled_subscriptions = []

# EXTRACT && TRANSFORM ------------------------------------------------------------------
hardware_sales_df = pd.read_excel(HARDWARE_DATA_PATH)
customer_df = pd.read_csv(CUSTOMER_DATA_PATH)

json_data, orders_data, cancelled_subscriptions = parse_event_json(json_file=SUBSCRIPTION_EVENTS_DATA_PATH)

# LOAD ------------------------------------------------------------------
subscription_events_df = pd.DataFrame(data=json_data)

cancellation_rate = cancellation_rate(subscription_events_df, cancelled_subscriptions)

calculate_lifetime_value(subscription_events_df)
calculate_total_revenue_to_date(subscription_events_df, hardware_sales_df)
