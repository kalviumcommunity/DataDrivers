import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).parent
PROCESSED = BASE_DIR / "data" / "processed"
REPORTS = PROCESSED / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

SEGMENTED = PROCESSED / "segmented_data.csv"
KPIS = PROCESSED / "kpis.csv"
VOL = PROCESSED / "volatility.csv"

SEGMENT_ORDER = ["Online TA", "Offline TA/TO", "Groups", "Direct", "Corporate", "Other"]
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2", "#937860"]


def load():
    df = pd.read_csv(SEGMENTED)
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
    kpi = pd.read_csv(KPIS) if KPIS.exists() else None
    vol = pd.read_csv(VOL) if VOL.exists() else None
    return df, kpi, vol


def save(fig, name):
    fig.tight_layout()
    fig.savefig(REPORTS / name, dpi=150)
    plt.close(fig)
    print(f"Saved: {name}")


def dataset_overview(df):
    print(df.info())
    print(df.describe(include="all"))
    print(df.isnull().sum())


def bookings_by_segment(df):
    counts = df["customer_segment"].value_counts().reindex(SEGMENT_ORDER).dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(counts.index, counts.values, color=PALETTE)
    ax.set_title("Total Bookings by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Bookings")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(ax.patches, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f"{int(val):,}", ha="center", va="bottom", fontsize=9)
    save(fig, "bookings_by_segment.png")


def bookings_by_hotel(df):
    counts = df["hotel"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values, color=PALETTE[:2])
    ax.set_title("Total Bookings by Hotel Type", fontsize=13, fontweight="bold")
    ax.set_xlabel("Hotel Type")
    ax.set_ylabel("Number of Bookings")
    for bar, val in zip(ax.patches, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f"{int(val):,}", ha="center", va="bottom", fontsize=9)
    save(fig, "bookings_by_hotel.png")


def monthly_bookings(df):
    m = df.groupby(df["reservation_status_date"].dt.to_period("M")).size()
    fig, ax = plt.subplots(figsize=(12, 5))
    m.plot(ax=ax, color="#4C72B0", linewidth=1.5)
    ax.set_title("Monthly Booking Trend", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Bookings")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    save(fig, "monthly_booking_trend.png")


def cancellation(df):
    rate = (
        df.groupby("customer_segment")["is_canceled"]
        .mean()
        .mul(100)
        .reindex(SEGMENT_ORDER)
        .dropna()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(rate.index, rate.values, color=PALETTE)
    ax.set_title("Cancellation Rate by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Cancellation Rate (%)")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(ax.patches, rate.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=9)
    save(fig, "cancellation_rate.png")


def adr(df):
    avg = (
        df.groupby("customer_segment")["adr"]
        .mean()
        .reindex(SEGMENT_ORDER)
        .dropna()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(avg.index, avg.values, color=PALETTE)
    ax.set_title("Average Daily Rate (ADR) by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average ADR (€)")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(ax.patches, avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"€{val:.1f}", ha="center", va="bottom", fontsize=9)
    save(fig, "adr_by_segment.png")


def revenue(df):
    d = df.copy()
    d["revenue_lost"] = (
        d["adr"] * (d["stays_in_week_nights"] + d["stays_in_weekend_nights"]) * d["is_canceled"]
    )
    totals = (
        d.groupby("customer_segment")["revenue_lost"]
        .sum()
        .reindex(SEGMENT_ORDER)
        .dropna()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(totals.index, totals.values, color=PALETTE)
    ax.set_title("Revenue Lost to Cancellations by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Revenue Lost (€)")
    ax.tick_params(axis="x", rotation=30)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"€{x/1e6:.1f}M"))
    for bar, val in zip(ax.patches, totals.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50000,
                f"€{val/1e6:.2f}M", ha="center", va="bottom", fontsize=8)
    save(fig, "revenue_lost.png")


def volatility_by_segment(vol):
    """Bar chart: Customer Segment vs Volatility Score (sorted descending)."""
    if vol is None:
        return
    data = vol.sort_values("volatility_score", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(data["customer_segment"], data["volatility_score"], color=PALETTE)
    ax.set_title("Occupancy Volatility Score by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Volatility Score (Std Dev of Monthly Cancellation Rate)")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(ax.patches, data["volatility_score"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom", fontsize=9)
    save(fig, "volatility.png")


def monthly_cancellation_by_segment(df):
    """Line chart: Monthly Cancellation Trend by Customer Segment."""
    df = df.copy()
    df["year_month"] = df["reservation_status_date"].dt.to_period("M")
    monthly = (
        df.groupby(["year_month", "customer_segment"])["is_canceled"]
        .mean()
        .mul(100)
        .reset_index()
    )
    monthly["year_month"] = monthly["year_month"].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(13, 6))
    for i, seg in enumerate(SEGMENT_ORDER):
        seg_data = monthly[monthly["customer_segment"] == seg].sort_values("year_month")
        if seg_data.empty:
            continue
        ax.plot(seg_data["year_month"], seg_data["is_canceled"],
                label=seg, color=PALETTE[i], linewidth=1.5)

    ax.set_title("Monthly Cancellation Rate Trend by Customer Segment", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Cancellation Rate (%)")
    ax.legend(title="Customer Segment", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    save(fig, "monthly_cancellation_by_segment.png")


def correlation(df):
    corr = df.select_dtypes("number").corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns, fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Feature Correlation Heatmap", fontsize=13, fontweight="bold")
    save(fig, "correlation_heatmap.png")


def insights(df):
    top = df["customer_segment"].value_counts().idxmax()
    highest_cancel = (
        df.groupby("customer_segment")["is_canceled"].mean().idxmax()
    )
    with open(REPORTS / "business_insights.txt", "w") as f:
        f.write(f"Highest booking segment: {top}\n")
        f.write(f"Highest cancellation rate segment: {highest_cancel}\n")
        f.write("Use dashboard filters to explore cancellation and ADR trends.\n")


def main():
    df, kpi, vol = load()
    dataset_overview(df)
    bookings_by_segment(df)
    bookings_by_hotel(df)
    monthly_bookings(df)
    cancellation(df)
    adr(df)
    revenue(df)
    volatility_by_segment(vol)
    monthly_cancellation_by_segment(df)
    correlation(df)
    insights(df)
    print(f"\nEDA complete. Reports saved to {REPORTS}")


if __name__ == "__main__":
    main()