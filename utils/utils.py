import matplotlib.pyplot as plt
import json
import pandas as pd


def extract(SUBSCRIPTION_EVENTS_DATA_PATH, HARDWARE_DATA_PATH):
    """
    Extracts the data from different sources and gets the data ready for processing

    :param SUBSCRIPTION_EVENTS_DATA_PATH: the path ot the subscription events file
    :param HARDWARE_DATA_PATH: the path ot the hardware events file

    :return:json_data, orders_data, cancelled_subscriptions and hardware_df
    """
    hardware_sales_df = pd.read_excel(HARDWARE_DATA_PATH)
    json_data, orders_data, cancelled_subscriptions = parse_event_json(json_file=SUBSCRIPTION_EVENTS_DATA_PATH)

    return json_data, orders_data, cancelled_subscriptions, hardware_sales_df


def parse_event_json(json_file: str):
    """
    Parses the event JSON file and enriches event data with supplementary customer data.

    We return the parsed json_data, the supplementary orders data anda list of cancelled subscriptions
    :param json_file: A string representation of the json file to be parsed/processed

    :return: json_data, orders_data, cancelled_subscriptions
    """
    print("Parsing event JSON.")
    json_data = []
    orders_data = {}
    cancelled_subscriptions = []

    with open(json_file, 'r') as subscription_events_file:
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

    print("Successfully parsed event JSON.")
    return json_data, orders_data, cancelled_subscriptions


def plot_revenue_sum(total_created_revenue, total_renewed_revenue, hardware_revenue):
    """
    Plot the total revenue to date for created subscriptions, renewals and hardware purchases

    :return:
    """
    print("Plotting total revenue.")
    plt.figure(2)
    plt.bar(['Created', 'Renewed', 'Hardware'], [total_created_revenue, total_renewed_revenue, hardware_revenue])
    plt.xlabel('Event Type')
    plt.ylabel('Revenue')
    plt.title('Revenue to date')
    plt.savefig("bi-output/revenue_to_date.png")


def plot_cumulative_sum(df_filtered_created, df_filtered_renewed, df_filtered_cancelled):
    """
    Plot the cumulative sum of revenue for created, renewed and hardware sales
    :return:
    """
    print("Plotting cumulative revenue.")
    plt.figure(3)
    plt.xlabel('Time')
    plt.ylabel('Revenue')
    plt.title('Cumulative Revenue to date')
    cumulative_total_created_revenue = df_filtered_created["revenue"].cumsum().plot(legend=True)
    cumulative_total_renewed_revenue = df_filtered_renewed["revenue"].cumsum().plot(legend=True)
    cumulative_total_hardware_revenue = df_filtered_cancelled["revenue"].cumsum().plot(legend=True)
    # cumulative_total_cancelled_revenue = df_filtered_cancelled["revenue"].cumsum().plot()
    plt.legend(["Created", "Renewals", "Hardware"])
    plt.savefig("bi-output/cumulative_sum.png")


def cancellation_rate(dataframe, cancelled_subscriptions) -> float:
    """
    Calculates the cancellation rate using the provided data frame.
    Using the formula: cancellation_rate = 1 - [(total_unique_orders - total_cancellations)/total_unique_orders]

    :param: dataframe - pandas dataframe object with the event data
    :param: cancelled_subscriptions - list of cancelled subscriptions captured when loading

    :return: A float value representing the cancellation rate
    """

    print("Plotting cancellation rate.")
    total_unique_orders = len(dataframe["order_id"].unique())
    cancelled_subscriptions = len(cancelled_subscriptions)

    cancellation_rate = 1 - (total_unique_orders - cancelled_subscriptions) / total_unique_orders

    values = [cancellation_rate, 1 - cancellation_rate]
    labels = ["Cancelled Subscriptions", "Active Subscriptions"]

    plt.figure(1)
    plt.title('Active vs. Cancelled subscriptions')
    pie_chart = plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.legend(pie_chart[0], labels, loc="best")
    plt.savefig("bi-output/cancellation_rate.png")

    return cancellation_rate


def calculate_lifetime_value(subscription_events_df):
    """
    Calculates the lifetime value per customer and orders in descending order

    :param: subscription_events_df: data frame containing subscription events

    :return: No return, just calculates and plots the lifetime cumulative value
    """
    plt.figure(4)
    lifetime_value = subscription_events_df.groupby("customer_id")["revenue"].sum().sort_values(ascending=False).head(10)
    lifetime_value.plot(x='customer_id', y='revenue', kind='bar')
    plt.savefig("bi-output/lifetime.png")
    print("The top 10 customers and their lifetime values are:")
    print(lifetime_value)


def calculate_total_revenue_to_date(subscription_events_df, hardware_sales_df):
    """
    Calculates the total revenue to date for created subscription, renewal and hardware events

    :param: subscription_events_df: data frame containing subscription events
    :param: hardware_sales_df: data frame containing hardware sales events

    :return: No return, just plots and saves the revenue to date graph
    """
    print("Calculating total revenue to date.")

    # Hardware Events
    hardware_revenue = hardware_sales_df["revenue"].sum()

    # Subscription Created
    df_filtered_created = subscription_events_df[subscription_events_df["event_type"] == "subscription_created"]
    total_created_revenue = df_filtered_created["revenue"].sum()

    # Subscription Renewed
    df_filtered_renewed = subscription_events_df[subscription_events_df["event_type"] == "subscription_renewed"]
    total_renewed_revenue = df_filtered_renewed["revenue"].sum()

    # Subscription Cancelled
    df_filtered_cancelled = subscription_events_df[subscription_events_df["event_type"] == "subscription_cancelled"]
    total_cancelled_revenue = df_filtered_cancelled["revenue"].sum()

    plot_revenue_sum(total_created_revenue, total_renewed_revenue, hardware_revenue)
    plot_cumulative_sum(df_filtered_created, df_filtered_renewed, df_filtered_cancelled)
    print("Successfully calculated total revenue to date.")