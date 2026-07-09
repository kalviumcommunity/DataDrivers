# Interactive Revenue Analytics Dashboard

This Product Requirement Document (PRD) outlines the development of an Interactive Revenue Analytics Dashboard. The tool will enable revenue teams to clean disparate booking data, segment customer behavior, and isolate the exact drivers of occupancy volatility.

# Product Requirement Document (PRD)

## 1. Product Overview

### 1.1 Objective

Build an internal data analytics platform and interactive web application. The platform will ingest raw booking, cancellation, and pricing data to surface actionable insights regarding customer-driven occupancy volatility.

By identifying high-risk customer segments, the dashboard will help revenue managers reduce occupancy volatility, improve pricing decisions, and minimize revenue loss from cancellations.

### 1.2 Target User

**Hotel Revenue Managers:** Needs to identify volatile customer segments to optimize pricing and forecasting.

**Operations Leads:** Needs predictable occupancy metrics to optimize staffing and inventory.

### 1.3 Success Metrics

**Time to Insight:** Reduce time spent manually matching segments from days to under 5 seconds.

**Segmentation Accuracy:** Achieve consistent and rule-based classification of historical bookings into predefined customer segments.

---

## 2. Technical Stack Mapping

The product relies on four distinct technical pillars to bridge the data-to-insight gap:

```text
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ 1. Data Cleaning     │ ──► │ 2. SQL Aggregation   │ ──► │ 3. Analysis & EDA    │ ──► │ 4. Streamlit App     │
│ (Concepts 6–16)      │     │ (Concepts 27–34)     │     │ (Concepts 22–26)     │     │ (Concepts 41–46)     │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

---

## 3. Functional Requirements

### Feature 1: Data Standardization Engine (Concepts 6–16)

**Input:** Raw, messy CSV/JSON exports of booking trends, cancellation history, and seasonal pricing.

#### Functional Needs:

- Resolve missing values in cancellation dates using imputation or strict flag tagging.
- Standardize date-time formats across mismatched data sources.
- Handle outliers, such as bulk group bookings that skew average lead times. [1]

---

### Feature 2: Segment Aggregation Layer (Concepts 27–34)

**Input:** Cleaned relational database tables.

#### Functional Needs:

- Execute complex SQL queries utilizing CASE WHEN logic to dynamically bucket users into segments (e.g., Corporate, Transient, OTA, Leisure).
- Calculate rolling cancellation rates for each customer segment using SQL aggregation techniques.
- Join disparate pricing and booking tables on hotel_id and booking_date without data duplication.

---

### Feature 3: Volatility Behavior Profiler (Concepts 22–26)

**Input:** Aggregated segment tables.

#### Functional Needs:

- Calculate statistical variance and standard deviation of occupancy metrics grouped by segment.
- Perform Exploratory Data Analysis (EDA) to find correlations between seasonal price hikes and cancellation spikes.
- Isolate the "Net Revenue Contribution" of segments vs. their "Volatility Metric".

---

### Feature 4: Revenue Cockpit App (Concepts 41–46)

**Input:** Statistical backend scripts.

#### Functional Needs:

- Build a responsive Streamlit web application.
- Include sidebar filters for Date Range, Hotel Location, and Booking Channel.
- Render interactive charts showing booking curves, cancellation distributions, and volatility heatmaps.

---

## 4. User Interface (UI) & Flow

- **Sidebar:** User selects the target date range and filters specific hotel properties.
- **Top KPI Cards:** Displays Global Occupancy Rate, Highest Volatility Segment, and Revenue Lost to Cancellations.
- **Main Body - Chart A:** A time-series line chart highlighting occupancy fluctuations over the selected period.
- **Main Body - Chart B:** A scatter plot mapping customer segments (X-axis: Revenue Contributed, Y-axis: Volatility Score) to instantly highlight high-value, high-risk groups.

---

## 5. Non-Functional Requirements

**Performance:** Streamlit app filters adjustments must recalculate and rerender charts in less than 2 seconds.

**Data Security:** Data must be processed locally or via secure internal servers; no public caching of proprietary pricing matrix data.

---

## 6. Scope

### In Scope:

- Historical booking analysis
- Customer segmentation
- Cancellation trend analysis
- Interactive Streamlit dashboard

### Out of Scope:

- Real-time booking integration
- Payment processing
- Predictive machine learning models
- Mobile application development

---

## 7. Assumptions

- Historical booking data is available.
- Customer segment information can be derived from booking attributes.
- Pricing and cancellation records are complete for the selected analysis period.

---

## Team Members

- Sibiraj
- Mithun
- Hariharan