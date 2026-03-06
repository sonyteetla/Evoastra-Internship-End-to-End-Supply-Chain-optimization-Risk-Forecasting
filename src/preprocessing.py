"""Data preprocessing module for supply chain capstone."""

import pandas as pd
import numpy as np
from typing import Tuple


def load_data(filepath: str) -> pd.DataFrame:
    """Load raw dataset from CSV."""
    return pd.read_csv(filepath, parse_dates=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the dataset."""
    # TODO: Implement cleaning logic
    pass
