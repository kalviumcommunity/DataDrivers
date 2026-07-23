import os
import sqlite3
from typing import Dict, Optional

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SOURCE_FILE = os.path.join(PROCESSED_DIR, "segmented_data.csv")
SQL_OUTPUT_DIR = os.path.join(PROCESSED_DIR, "sql_outputs")


def _load_processed_data(processed_file: str = SOURCE_FILE) -> pd.DataFrame:
	"""
	Loads the processed, segmented dataset created by the main pipeline.
	"""
	if not os.path.exists(processed_file):
		raise FileNotFoundError(
			"Processed segmented data not found. Run the main pipeline first: "
			f"{processed_file}"
		)

	df = pd.read_csv(processed_file)

	if "reservation_status_date" in df.columns:
		df["reservation_status_date"] = pd.to_datetime(
			df["reservation_status_date"],
			errors="coerce"
		)

	return df


def _prepare_sqlite_connection(df: pd.DataFrame) -> sqlite3.Connection:
	"""
	Creates an in-memory SQLite database and loads the processed bookings table.
	"""
	conn = sqlite3.connect(":memory:")
	bookings_df = df.copy()

	if "reservation_status_date" in bookings_df.columns:
		bookings_df["reservation_status_date"] = bookings_df[
			"reservation_status_date"
		].dt.strftime("%Y-%m-%d")

	bookings_df.to_sql("bookings", conn, if_exists="replace", index=False)
	return conn


def _run_query_and_save(
	conn: sqlite3.Connection,
	query_name: str,
	query: str,
	output_dir: str = SQL_OUTPUT_DIR,
) -> pd.DataFrame:
	"""
	Runs a SQL query, prints a preview, and saves the result to CSV.
	"""
	result = pd.read_sql_query(query, conn)

	os.makedirs(output_dir, exist_ok=True)
	output_file = os.path.join(output_dir, f"{query_name}.csv")
	result.to_csv(output_file, index=False)

	print(f"\n{query_name.replace('_', ' ').title()}")
	print("-" * 40)
	if result.empty:
		print("No rows returned.")
	else:
		print(result.head().to_string(index=False))
	print(f"Saved to: {output_file}")

	return result


def run_sql_aggregations(
	df: Optional[pd.DataFrame] = None,
	processed_file: str = SOURCE_FILE,
	output_dir: str = SQL_OUTPUT_DIR,
) -> Dict[str, pd.DataFrame]:
	"""
	Builds SQL business summaries from the processed pipeline output.
	"""
	if df is None:
		df = _load_processed_data(processed_file)

	conn = _prepare_sqlite_connection(df)

	queries = [
		(
			"total_bookings_by_customer_segment",
			# Counts all bookings per standardized customer segment.
			"""
			-- Total bookings by customer segment
			SELECT
				customer_segment,
				COUNT(*) AS total_bookings
			FROM bookings
			GROUP BY customer_segment
			ORDER BY total_bookings DESC, customer_segment ASC;
			""",
		),
		(
			"cancellation_rate_by_customer_segment",
			# Measures the share of canceled bookings in each customer segment.
			"""
			-- Cancellation rate by customer segment
			SELECT
				customer_segment,
				ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2) AS cancellation_rate
			FROM bookings
			GROUP BY customer_segment
			ORDER BY cancellation_rate DESC, customer_segment ASC;
			""",
		),
		(
			"average_adr_by_customer_segment",
			# Calculates the average daily rate by customer segment.
			"""
			-- Average ADR by customer segment
			SELECT
				customer_segment,
				ROUND(AVG(adr), 2) AS average_adr
			FROM bookings
			GROUP BY customer_segment
			ORDER BY average_adr DESC, customer_segment ASC;
			""",
		),
		(
			"revenue_lost_by_customer_segment",
			# Estimates revenue lost from canceled stays by customer segment.
			"""
			-- Revenue lost by customer segment
			SELECT
				customer_segment,
				ROUND(
					SUM(
						CASE
							WHEN is_canceled = 1 THEN adr * (
								stays_in_weekend_nights + stays_in_week_nights
							)
							ELSE 0
						END
					),
					2
				) AS revenue_lost
			FROM bookings
			GROUP BY customer_segment
			ORDER BY revenue_lost DESC, customer_segment ASC;
			""",
		),
		(
			"monthly_booking_summary",
			# Summarizes monthly booking volume, cancellations, pricing, and lost revenue.
			"""
			-- Monthly booking summary
			SELECT
				strftime('%Y-%m', reservation_status_date) AS booking_month,
				COUNT(*) AS total_bookings,
				SUM(is_canceled) AS canceled_bookings,
				ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2) AS cancellation_rate,
				ROUND(AVG(adr), 2) AS average_adr,
				ROUND(
					SUM(
						CASE
							WHEN is_canceled = 1 THEN adr * (
								stays_in_weekend_nights + stays_in_week_nights
							)
							ELSE 0
						END
					),
					2
				) AS revenue_lost
			FROM bookings
			WHERE reservation_status_date IS NOT NULL
			GROUP BY booking_month
			ORDER BY booking_month ASC;
			""",
		),
		(
			"hotel_wise_booking_summary",
			# Compares booking volume and performance metrics across hotel types.
			"""
			-- Hotel-wise booking summary
			SELECT
				hotel,
				COUNT(*) AS total_bookings,
				SUM(is_canceled) AS canceled_bookings,
				ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2) AS cancellation_rate,
				ROUND(AVG(adr), 2) AS average_adr,
				ROUND(
					SUM(
						CASE
							WHEN is_canceled = 1 THEN adr * (
								stays_in_weekend_nights + stays_in_week_nights
							)
							ELSE 0
						END
					),
					2
				) AS revenue_lost
			FROM bookings
			GROUP BY hotel
			ORDER BY total_bookings DESC, hotel ASC;
			""",
		),
	]

	results: Dict[str, pd.DataFrame] = {}
	try:
		for query_name, query in queries:
			results[query_name] = _run_query_and_save(conn, query_name, query, output_dir)
	finally:
		conn.close()

	return results


if __name__ == "__main__":
	print("Loading processed data for SQL aggregations...")
	run_sql_aggregations()