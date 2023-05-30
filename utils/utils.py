import matplotlib.pyplot as plt
import json

def load():
    """

    :return:
    """

    pass

def extract():
    """

    :return:
    """
    pass


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
    :return: None
    """
    print("Plotting cumulative revenue.")
    plt.figure(3)
    cumulative_total_created_revenue = df_filtered_created["revenue"].cumsum().plot()
    cumulative_total_renewed_revenue = df_filtered_renewed["revenue"].cumsum().plot()
    cumulative_total_hardware_revenue = df_filtered_cancelled["revenue"].cumsum().plot()
    # cumulative_total_cancelled_revenue = df_filtered_cancelled["revenue"].cumsum().plot()
    plt.savefig("bi-output/cumulative_sum.png")
    pass


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
    pie_chart = plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.legend(pie_chart[0], labels, loc="best")
    plt.savefig("bi-output/cancellation_rate.png")

    return cancellation_rate

def parse_event_json(json_file):
    """
    Parses the event JSON file and enriches event data with supplementary customer data
    :param json_file:
    :return:
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


def calculate_lifetime_value(dataframe):
    """
    Calculates the lifetime value per customer and orders in descending order
    :param dataframe:
    :return:
    """
    lifetime_value = dataframe.groupby("customer_id")["revenue"].sum().sort_values(ascending=False)
    return