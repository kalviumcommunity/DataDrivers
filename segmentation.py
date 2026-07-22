import pandas as pd

def segment_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes and groups the `market_segment` column.
    """
    df = df.copy()
    
    # Map raw market segments to broader categories
    segment_mapping = {
        'Online TA': 'Online TA',
        'Offline TA/TO': 'Offline TA/TO',
        'Groups': 'Groups',
        'Direct': 'Direct',
        'Corporate': 'Corporate',
        'Complementary': 'Other',
        'Aviation': 'Other',
        'Undefined': 'Other'
    }
    
    if 'market_segment' in df.columns:
        df['customer_segment'] = df['market_segment'].map(segment_mapping).fillna('Other')
    else:
        df['customer_segment'] = 'Unknown'
        
    return df
