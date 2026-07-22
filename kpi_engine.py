import pandas as pd
import numpy as np

def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates key metrics per customer segment.
    """
    kpis = []
    
    if 'customer_segment' not in df.columns:
        return pd.DataFrame()
        
    segments = df['customer_segment'].unique()
    
    for segment in segments:
        segment_df = df[df['customer_segment'] == segment]
        
        total_bookings = len(segment_df)
        canceled_bookings = segment_df['is_canceled'].sum() if 'is_canceled' in segment_df.columns else 0
        
        # Occupancy Rate (Successful stays / Total bookings)
        successful_stays = total_bookings - canceled_bookings
        occupancy_rate = (successful_stays / total_bookings)*100 if total_bookings > 0 else 0
        
        # Cancellation Rate
        cancellation_rate = (canceled_bookings / total_bookings)*100 if total_bookings > 0 else 0
        
        # ADR (AverageDailyRate)
        adr = segment_df['adr'].mean() if 'adr' in segment_df.columns else 0
        
        # Revenue Lost to Cancellations
        revenue_lost = 0
        if 'is_canceled' in segment_df.columns and 'adr' in segment_df.columns and 'stays_in_weekend_nights' in segment_df.columns and 'stays_in_week_nights' in segment_df.columns:
            segment_df_canceled = segment_df[segment_df['is_canceled'] == 1]
            total_nights_canceled = (segment_df_canceled['stays_in_weekend_nights'] + segment_df_canceled['stays_in_week_nights'])
            revenue_lost = (segment_df_canceled['adr'] * total_nights_canceled).sum()
        
        kpis.append({
            'customer_segment': segment,
            'total_bookings': total_bookings,
            'occupancy_rate': occupancy_rate,
            'cancellation_rate': cancellation_rate,
            'adr': adr,
            'revenue_lost': revenue_lost
        })
        
    return pd.DataFrame(kpis)
