from pathlib import Path

import pandas as pd


MONTH_MAP = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def load_data(input_path: Path) -> pd.DataFrame:
    return pd.read_csv(input_path)


def remove_duplicate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    duplicate_count = int(df.duplicated().sum())
    cleaned = df.drop_duplicates().copy()
    return cleaned, duplicate_count


def standardize_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    if "reservation_status_date" in cleaned.columns:
        cleaned["reservation_status_date"] = pd.to_datetime(
            cleaned["reservation_status_date"], errors="coerce"
        )

    if {
        "arrival_date_year",
        "arrival_date_month",
        "arrival_date_day_of_month",
    }.issubset(cleaned.columns):
        arrival_month = (
            cleaned["arrival_date_month"].astype(str).str.strip().str.lower().map(MONTH_MAP)
        )
        cleaned["arrival_date"] = pd.to_datetime(
            {
                "year": cleaned["arrival_date_year"],
                "month": arrival_month,
                "day": cleaned["arrival_date_day_of_month"],
            },
            errors="coerce",
        )
        cleaned["arrival_date_month"] = cleaned["arrival_date_month"].astype(str).str.strip().str.title()

    return cleaned


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing_counts = df.isna().sum()
    missing_columns = missing_counts[missing_counts > 0].sort_values(ascending=False)

    summary = pd.DataFrame(
        {
            "missing_count": missing_columns,
            "missing_percentage": (missing_columns / len(df) * 100).round(2),
        }
    )
    return summary


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    if "agent" in cleaned.columns:
        cleaned["agent"] = cleaned["agent"].fillna(0)

    if "company" in cleaned.columns:
        cleaned["company"] = cleaned["company"].fillna("Unknown")

    if "children" in cleaned.columns:
        cleaned["children"] = cleaned["children"].fillna(0)

    numeric_columns = cleaned.select_dtypes(include="number").columns
    for column in numeric_columns:
        if column in {"agent", "children"}:
            continue
        median_value = cleaned[column].median()
        cleaned[column] = cleaned[column].fillna(median_value)

    categorical_columns = cleaned.select_dtypes(include=["object", "string", "category"]).columns
    for column in categorical_columns:
        if column == "company":
            continue
        mode_values = cleaned[column].mode(dropna=True)
        if not mode_values.empty:
            cleaned[column] = cleaned[column].fillna(mode_values.iloc[0])

    return cleaned


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    if "adr" in cleaned.columns:
        cleaned = cleaned.loc[cleaned["adr"] >= 0].copy()

    return cleaned


def clean_dataset(input_path: Path) -> pd.DataFrame:
    df = load_data(input_path)
    df, _ = remove_duplicate_rows(df)
    df = standardize_date_columns(df)
    df = fill_missing_values(df)
    df = remove_invalid_rows(df)
    return df


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    input_path = project_root / "data" / "hotel_bookings.csv"
    output_path = project_root / "data" / "processed" / "cleaned_hotel_bookings.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    raw_df = load_data(input_path)

    deduped_df, duplicate_count = remove_duplicate_rows(raw_df)
    print(f"Duplicate booking records found: {duplicate_count}")
    print(f"Shape after duplicate removal: {deduped_df.shape}")

    print("Missing values before cleaning:")
    before_summary = missing_value_summary(raw_df)
    if before_summary.empty:
        print("No missing values found.")
    else:
        print(before_summary.to_string())

    cleaned_df = clean_dataset(input_path)

    print("\nMissing values after cleaning:")
    after_summary = missing_value_summary(cleaned_df)
    if after_summary.empty:
        print("No missing values found.")
    else:
        print(after_summary.to_string())

    cleaned_df.to_csv(output_path, index=False)

    print(f"Loaded data from: {input_path}")
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    print(f"Saved cleaned data to: {output_path}")


if __name__ == "__main__":
    main()