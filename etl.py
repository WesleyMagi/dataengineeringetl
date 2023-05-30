import pandas as pd
from utils.utils import cancellation_rate, calculate_lifetime_value, parse_event_json, \
    calculate_total_revenue_to_date, extract

HARDWARE_DATA_PATH = "data/hardware_sales.xlsx"
CUSTOMER_DATA_PATH = "data/customers.csv"
SUBSCRIPTION_EVENTS_DATA_PATH = "data/subscription_events.json"

json_data = []
orders_data = {}
cancelled_subscriptions = []

# EXTRACT && TRANSFORM ------------------------------------------------------------------
json_data, orders_data, cancelled_subscriptions, hardware_sales_df = extract(SUBSCRIPTION_EVENTS_DATA_PATH, HARDWARE_DATA_PATH)
hardware_sales_df = pd.read_excel(HARDWARE_DATA_PATH)

json_data, orders_data, cancelled_subscriptions = parse_event_json(json_file=SUBSCRIPTION_EVENTS_DATA_PATH)

# LOAD ------------------------------------------------------------------
subscription_events_df = pd.DataFrame(data=json_data)

cancellation_rate = cancellation_rate(subscription_events_df, cancelled_subscriptions)

calculate_lifetime_value(subscription_events_df)
calculate_total_revenue_to_date(subscription_events_df, hardware_sales_df)
