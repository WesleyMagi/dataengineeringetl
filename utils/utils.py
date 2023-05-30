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

def plot_revenue_sum():
    """
    Plots the revenue to a figure
    :return:
    """
    pass

def plot_cumulative_sum():
    """

    :return:
    """
    pass


def cancellation_rate(dataframe, cancelled_subscriptions) -> float:
    """
    Calculates the cancellation rate using the provided data frame.
    Using the formula: cancellation_rate = 1 - [(total_unique_orders - total_cancellations)/total_unique_orders]

    :param: dataframe - pandas dataframe object with the event data
    :param: cancelled_subscriptions - list of cancelled subscriptions captured when loading

    :return: A float value representing the cancellation rate
    """

    total_unique_orders = len(dataframe["order_id"].unique())
    cancelled_subscriptions = len(cancelled_subscriptions)

    cancellation_rate = 1 - (total_unique_orders - cancelled_subscriptions) / total_unique_orders

    values = [cancellation_rate, 1 - cancellation_rate]
    labels = ["Cancelled Subscriptions", "Active Subscriptions"]

    pie_chart = plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.legend(pie_chart[0], labels, loc="best")
    plt.show()

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