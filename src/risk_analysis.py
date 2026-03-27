import numpy as np


def monte_carlo_risk(delay_mean, delay_std, simulations=1000):

    delay_simulation = np.random.normal(
        delay_mean,
        delay_std,
        simulations
    )

    return delay_simulation