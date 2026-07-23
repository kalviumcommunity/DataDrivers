
# Validation Report — Hotel Customer Segment Analytics

**Generated:** 2025  
**Dataset:** data/processed/segmented_data.csv (119,210 rows, 34 columns, 0 nulls)

---

## 1. Charts Generated

All charts saved to data/processed/reports/.

| File | Title | Source |
|---|---|---|
| bookings_by_segment.png | Total Bookings by Customer Segment | segmented_data.csv |
| bookings_by_hotel.png | Total Bookings by Hotel Type | segmented_data.csv |
| monthly_booking_trend.png | Monthly Booking Trend | segmented_data.csv |
| cancellation_rate.png | Cancellation Rate by Customer Segment | segmented_data.csv |
| adr_by_segment.png | Average Daily Rate (ADR) by Customer Segment | segmented_data.csv |
| revenue_lost.png | Revenue Lost to Cancellations by Customer Segment | segmented_data.csv |
| volatility.png | Occupancy Volatility Score by Customer Segment | volatility.csv |
| monthly_cancellation_by_segment.png | Monthly Cancellation Rate Trend by Customer Segment | segmented_data.csv |
| correlation_heatmap.png | Feature Correlation Heatmap | segmented_data.csv |

### Chart Validation Notes

All bar charts now include axis labels (xlabel, ylabel), bold titles, and value annotations on each bar.
Cancellation rate, ADR, and revenue lost bars are sorted descending for immediate visual ranking.
Revenue lost y-axis uses M (millions) formatting for readability.
Correlation heatmap uses coolwarm diverging colormap with vmin=-1, vmax=1 for correct interpretation.
Monthly cancellation trend uses a consistent 6-colour palette per segment with a legend.
volatility.png is now sorted descending by volatility score (previously unsorted).
monthly_cancellation_by_segment.png is a **new chart** added in this validation pass.

---

## 2. SQL Aggregation Validation

SQL queries were executed in-memory via sql_aggregation.py against segmented_data.csv.  
Results compared against data/processed/sql_outputs/.

### Total Bookings by Segment

| Segment | SQL Count |
|---|---|
| Online TA | 56,408 |
| Offline TA/TO | 24,182 |
| Groups | 19,791 |
| Direct | 12,582 |
| Corporate | 5,282 |
| Other | 965 |

**Status: PASS** — All 6 segments present. Counts match segmented_data.csv row counts exactly.

### Cancellation Rate by Segment

| Segment | SQL Rate |
|---|---|
| Groups | 61.11% |
| Online TA | 36.76% |
| Offline TA/TO | 34.33% |
| Corporate | 18.76% |
| Direct | 15.37% |
| Other | 14.82% |

**Status: PASS** — All 6 segments present. Rates consistent with is_canceled column.

### Average ADR by Segment

| Segment | SQL ADR |
|---|---|
| Online TA | €117.32 |
| Direct | €115.63 |
| Offline TA/TO | €87.48 |
| Groups | €79.56 |
| Corporate | €69.53 |
| Other | €26.85 |

**Status: PASS** — All 6 segments present. Values consistent with adr column.

### Revenue Lost by Segment

| Segment | SQL Revenue Lost |
|---|---|
| Online TA | €10,227,646.11 |
| Groups | €2,800,543.98 |
| Offline TA/TO | €2,492,358.15 |
| Direct | €993,409.82 |
| Corporate | €196,383.07 |
| Other | €16,895.99 |

**Status: PASS** — All 6 segments present. Formula adr × (weekend_nights + week_nights) for canceled bookings is consistent with kpi_engine.py.

---

## 3. KPI Validation (kpis.csv vs SQL Outputs)

Cross-validation of kpis.csv (produced by kpi_engine.py) against SQL aggregation outputs.  
Tolerance: ±0.02 for floating-point comparisons.

| KPI | Direct | Corporate | Online TA | Offline TA/TO | Other | Groups |
|---|---|---|---|---|---|---|
| total_bookings | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK |
| cancellation_rate | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK |
| adr | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK |
| revenue_lost | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK | ✅ OK |

**All 24 KPI checks passed. No inconsistencies found.**

---

## 4. Inconsistencies Found

| # | Location | Issue | Severity |
|---|---|---|---|
| 1 | eda_analysis.py (original) | All bar charts missing xlabel and ylabel | Medium |
| 2 | eda_analysis.py (original) | volatility() plotted segments in unsorted order | Low |
| 3 | eda_analysis.py (original) | Cancellation, ADR, revenue bars not sorted — hardest to compare visually | Medium |
| 4 | eda_analysis.py (original) | Correlation heatmap used default colormap with no vmin/vmax — misleading scale | Medium |
| 5 | eda_analysis.py (original) | Revenue lost y-axis showed raw numbers (e.g. 10000000) — unreadable | Low |
| 6 | eda_analysis.py (original) | business_insights.txt only reported highest booking segment, not highest cancellation segment | Low |
| 7 | sql_aggregation.py monthly summary | reservation_status_date used as booking month proxy — this is the status date, not arrival date. Months with 100% cancellation rate (e.g. 2014-10) indicate the field captures cancellation/check-out dates, not booking creation dates | Medium |

**No data-level inconsistencies between kpis.csv and SQL outputs.**

---

## 5. Recommendations

1. **Groups segment is the highest volatility driver** (61.1% cancellation rate, volatility score 0.320). Revenue management should apply stricter deposit policies or non-refundable rates for group bookings.

2. **Online TA drives the most absolute revenue loss** (€10.2M) despite a moderate cancellation rate (36.8%), due to high booking volume. Consider dynamic pricing or cancellation fee tiers for this segment.

3. **Use arrival_date columns for monthly booking trend analysis** instead of reservation_status_date. The status date reflects when a booking was checked out or cancelled, not when it was made, causing misleading 100% cancellation months in the monthly summary SQL query.

4. **Corporate segment has the lowest volatility** (0.108) and a stable ADR (€69.53). This segment is a reliable occupancy anchor — consider loyalty or long-stay incentives to grow it.

5. **Other segment** (965 bookings, €26.85 ADR) has anomalously low ADR. Investigate whether this segment contains data quality issues or complimentary/staff bookings before including it in revenue forecasting.

6. **Dashboard filter priority**: Expose cancellation rate and volatility score as primary filters. These two metrics together identify which segments to target for pricing intervention.