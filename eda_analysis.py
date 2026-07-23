
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent
PROCESSED = BASE_DIR / "data" / "processed"
REPORTS = PROCESSED / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

SEGMENTED = PROCESSED / "segmented_data.csv"
KPIS = PROCESSED / "kpis.csv"
VOL = PROCESSED / "volatility.csv"

def load():
    df = pd.read_csv(SEGMENTED)
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
    kpi = pd.read_csv(KPIS) if KPIS.exists() else None
    vol = pd.read_csv(VOL) if VOL.exists() else None
    return df,kpi,vol

def save(fig,name):
    fig.tight_layout()
    fig.savefig(REPORTS/name,dpi=300)
    plt.close(fig)

def dataset_overview(df):
    print(df.info())
    print(df.describe(include="all"))
    print(df.isnull().sum())

def bookings_by_segment(df):
    fig,ax=plt.subplots(figsize=(8,5))
    df["customer_segment"].value_counts().plot(kind="bar",ax=ax)
    ax.set_title("Bookings by Customer Segment")
    save(fig,"bookings_by_segment.png")

def bookings_by_hotel(df):
    fig,ax=plt.subplots(figsize=(6,4))
    df["hotel"].value_counts().plot(kind="bar",ax=ax)
    ax.set_title("Bookings by Hotel")
    save(fig,"bookings_by_hotel.png")

def monthly_bookings(df):
    m=df.groupby(df["reservation_status_date"].dt.to_period("M")).size()
    fig,ax=plt.subplots(figsize=(10,5))
    m.plot(ax=ax)
    ax.set_title("Monthly Booking Trend")
    save(fig,"monthly_booking_trend.png")

def cancellation(df):
    rate=df.groupby("customer_segment")["is_canceled"].mean()*100
    fig,ax=plt.subplots(figsize=(8,5))
    rate.plot(kind="bar",ax=ax)
    ax.set_ylabel("Cancellation %")
    ax.set_title("Cancellation Rate by Segment")
    save(fig,"cancellation_rate.png")

def adr(df):
    fig,ax=plt.subplots(figsize=(8,5))
    df.groupby("customer_segment")["adr"].mean().plot(kind="bar",ax=ax)
    ax.set_title("Average ADR by Segment")
    save(fig,"adr_by_segment.png")

def revenue(df):
    d=df.copy()
    d["revenue_lost"]=d["adr"]*(d["stays_in_week_nights"]+d["stays_in_weekend_nights"])*d["is_canceled"]
    fig,ax=plt.subplots(figsize=(8,5))
    d.groupby("customer_segment")["revenue_lost"].sum().plot(kind="bar",ax=ax)
    ax.set_title("Revenue Lost by Segment")
    save(fig,"revenue_lost.png")

def volatility(vol):
    if vol is None: return
    fig,ax=plt.subplots(figsize=(8,5))
    vol.plot(x="customer_segment",y="volatility_score",kind="bar",ax=ax,legend=False)
    ax.set_title("Volatility by Segment")
    save(fig,"volatility.png")

def correlation(df):
    fig,ax=plt.subplots(figsize=(10,8))
    corr=df.select_dtypes("number").corr()
    im=ax.imshow(corr)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns,rotation=90,fontsize=8)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns,fontsize=8)
    fig.colorbar(im)
    ax.set_title("Correlation Heatmap")
    save(fig,"correlation_heatmap.png")

def insights(df):
    with open(REPORTS/"business_insights.txt","w") as f:
        top=df["customer_segment"].value_counts().idxmax()
        f.write(f"Highest booking segment: {top}\n")
        f.write("Use dashboard filters to explore cancellation and ADR trends.\n")

def main():
    df,kpi,vol=load()
    dataset_overview(df)
    bookings_by_segment(df)
    bookings_by_hotel(df)
    monthly_bookings(df)
    cancellation(df)
    adr(df)
    revenue(df)
    volatility(vol)
    correlation(df)
    insights(df)
    print("EDA complete. Reports saved to",REPORTS)

if __name__=="__main__":
    main()
