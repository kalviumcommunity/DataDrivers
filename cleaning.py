import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw Hotel Booking Demand dataset.
    """
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # Fill missing values
    if 'children' in df.columns:
        df['children'] = df['children'].fillna(0).astype(int)
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('Unknown')
    if 'agent' in df.columns:
        df['agent'] = df['agent'].fillna(0)
    if 'company' in df.columns:
        df['company'] = df['company'].fillna(0)

    # Convert datatypes
    if 'reservation_status_date' in df.columns:
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

    # Remove invalid rows (e.g., zero guests)
    if all(c in df.columns for c in ['adults', 'children', 'babies']):
        df['total_guests'] = df['adults'] + df['children'] + df['babies']
        df = df[df['total_guests'] > 0]

    return df
