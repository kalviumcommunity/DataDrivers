import pandas as pd

def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a volatility score (standard deviation of cancellations) per customer segment over time.
    """
    if 'reservation_status_date' not in df.columns or 'customer_segment' not in df.columns or 'is_canceled' not in df.columns:
        return pd.DataFrame()
        
    df = df.copy()
    
    # Create a Year-Month column for grouping
    df['year_month'] = df['reservation_status_date'].dt.to_period('M')
    
    # Calculate monthly cancellation rates per segment
    monthly_cancellations = df.groupby(['customer_segment', 'year_month'])['is_canceled'].mean().reset_index()
    
    # Volatility is the standard deviation of the monthly cancellation rate
    volatility = monthly_cancellations.groupby('customer_segment')['is_canceled'].std().reset_index()
    volatility.rename(columns={'is_canceled': 'volatility_score'}, inplace=True)
    
    # Fill NaN for segments with only one month of data (std is NaN for N=1)
    volatility['volatility_score'] = volatility['volatility_score'].fillna(0)
    
    return volatility
