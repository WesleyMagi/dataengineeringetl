import matplotlib.pyplot as plt

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
    pass


def calculate_lifetime_value(dataframe):
    """
    Calculates the lifetime value per customer and orders in descending order
    :param dataframe:
    :return:
    """
    lifetime_value = dataframe.groupby("customer_id")["revenue"].sum().sort_values(ascending=False)
    return