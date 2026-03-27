import pandas as pd


def load_data(path):
    df = pd.read_csv(path)
    return df


def preprocess_data(df):

    df['shipping_delay'] = (
        df['days_for_shipping_real'] -
        df['days_for_shipment_scheduled']
    )

    df['profit_margin'] = (
        df['order_profit_per_order'] /
        df['sales']
    )

    df['sales_per_item'] = (
        df['sales'] / df['order_item_quantity']
    )

    return df