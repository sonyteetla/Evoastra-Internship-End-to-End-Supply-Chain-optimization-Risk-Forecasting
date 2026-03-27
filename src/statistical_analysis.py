from scipy import stats
import pandas as pd


def anova_shipping_delay(df):

    groups = [
        group["shipping_delay"].values
        for name, group in df.groupby("shipping_mode")
    ]

    f_stat, p_value = stats.f_oneway(*groups)

    return f_stat, p_value


def chi_square_category_delay(df):

    cont_table = pd.crosstab(
        df['category_name'],
        df['late_delivery_risk']
    )

    chi2, p, dof, expected = stats.chi2_contingency(cont_table)

    return chi2, p