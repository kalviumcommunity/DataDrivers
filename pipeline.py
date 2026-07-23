import os
import pandas as pd
import streamlit as st

from cleaning import clean_data
from sql_aggregation import run_sql_aggregations
from segmentation import segment_customers
from kpi_engine import calculate_kpis
from volatility import calculate_volatility


@st.cache_data
def load_and_process_data(file_path: str):
    """
    Loads raw data and runs the entire pipeline.
    Saves processed outputs to data/processed/.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    print(f"Loading dataset from: {file_path}")

    # Step 1: Load data
    df = pd.read_csv(file_path)

    print(f"Dataset loaded successfully.")
    print(f"Shape: {df.shape}")

    # Step 2: Clean data
    print("Cleaning data...")
    cleaned_df = clean_data(df)

    # Step 3: Segment customers
    print("Segmenting customers...")
    segmented_df = segment_customers(cleaned_df)

    # Step 4: Calculate KPIs
    print("Calculating KPIs...")
    kpis_df = calculate_kpis(segmented_df)

    # Step 5: Calculate volatility
    print("Calculating volatility scores...")
    volatility_df = calculate_volatility(segmented_df)

    # Step 6: Run SQL business aggregations against the processed dataset.
    print("Running SQL aggregations...")
    sql_results = run_sql_aggregations(segmented_df)

    # Step 7: Save outputs
    data_dir = os.path.dirname(file_path)
    output_dir = os.path.join(data_dir, "processed")

    os.makedirs(output_dir, exist_ok=True)

    cleaned_df.to_csv(
        os.path.join(output_dir, "cleaned_data.csv"),
        index=False
    )

    segmented_df.to_csv(
        os.path.join(output_dir, "segmented_data.csv"),
        index=False
    )

    kpis_df.to_csv(
        os.path.join(output_dir, "kpis.csv"),
        index=False
    )

    volatility_df.to_csv(
        os.path.join(output_dir, "volatility.csv"),
        index=False
    )

    print(f"All files saved to: {output_dir}")

    return segmented_df, kpis_df, volatility_df, sql_results


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Dataset path
    raw_data_path = os.path.join(
        current_dir,
        "data",
        "hotel_bookings.csv"
    )

    try:
        print("=" * 60)
        print("HOTEL BOOKING DATA PIPELINE")
        print("=" * 60)

        segmented_df, kpis_df, volatility_df, sql_results = load_and_process_data(
            raw_data_path
        )

        print("\nPipeline executed successfully!")
        print(f"Total records processed: {len(segmented_df)}")

        print("\nKPI Preview")
        print("-" * 40)
        print(kpis_df.head())

        print("\nVolatility Preview")
        print("-" * 40)
        print(volatility_df.head())

        print("\nSQL Output Files Generated:")
        print("data/processed/sql_outputs/total_bookings_by_customer_segment.csv")
        print("data/processed/sql_outputs/cancellation_rate_by_customer_segment.csv")
        print("data/processed/sql_outputs/average_adr_by_customer_segment.csv")
        print("data/processed/sql_outputs/revenue_lost_by_customer_segment.csv")
        print("data/processed/sql_outputs/monthly_booking_summary.csv")
        print("data/processed/sql_outputs/hotel_wise_booking_summary.csv")

        print("\nOutput Files Generated:")
        print("data/processed/cleaned_data.csv")
        print("data/processed/segmented_data.csv")
        print("data/processed/kpis.csv")
        print("data/processed/volatility.csv")
        print("data/processed/sql_outputs/")

    except FileNotFoundError as e:
        print("\nERROR:")
        print(e)

        print("\nExpected dataset location:")
        print(raw_data_path)

    except Exception as e:
        print("\nPIPELINE FAILED")
        print(f"Error: {e}")