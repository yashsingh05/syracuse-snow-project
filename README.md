\# Syracuse Winter Operations Pipeline



An automated data pipeline analyzing snowplow service equity across Syracuse, NY neighborhoods, using live city open data.



\## What this does



Every day, an automated job pulls the City of Syracuse's live snow-route status data (plow pass counts, last-serviced timestamps, road priority classification) and saves a snapshot. Separately, five years of 311 service complaints and official neighborhood boundaries are loaded and spatially joined, so complaint volume and road classification can be analyzed at the neighborhood level.



\*\*Core question:\*\* Does snowplow response — and the underlying road-priority classification that determines it — vary systematically by neighborhood?



\## Architecture



\- \*\*Ingestion:\*\* Python script polls Syracuse's public ArcGIS FeatureServer for snow route status

\- \*\*Automation:\*\* Hosted on PythonAnywhere (free tier), triggered daily via an external cron service (cron-job.org), since PythonAnywhere's own scheduler requires a paid plan

\- \*\*Storage:\*\* DuckDB

\- \*\*Transformation:\*\* dbt (staging models + spatial mart models)

\- \*\*Data quality:\*\* 10 dbt tests covering null checks, uniqueness, and accepted values



\## Data sources



\- `Winter\_Operations\_Snow\_Routes` — 5,017 road segments with plow status, pass counts, priority classification

\- `SYRCityline\_Requests\_2021\_Present` — 654 snow/ice-related 311 complaints (2021–present)

\- `Syracuse\_Neighborhoods` — 32 official neighborhood boundary polygons



\## Findings so far (pre-winter)



\- \*\*Complaint volume by neighborhood\*\* — Eastwood, Northside, and Meadowbrook generate the most snow/ice-related 311 complaints since 2021

\- \*\*Structural priority disparity\*\* — South Campus (95.9%), Franklin Square (89.1%), and Eastwood (83.3%) have the highest share of "Priority 2" (lower-priority) streets, meaning these neighborhoods are structurally positioned for slower plow response regardless of actual crew behavior

\- Eastwood appears at the top of both lists — high complaint volume and heavy Priority-2 classification — a notable overlap worth investigating further once winter response-time data is available



\## Notable engineering challenges solved



\- \*\*PythonAnywhere `sys.executable` bug:\*\* the standard Python way of referencing the current interpreter resolves incorrectly inside PythonAnywhere's web app environment (returns the `uwsgi` process instead), silently breaking subprocess calls. Fixed by hardcoding the interpreter path.

\- \*\*Coordinate axis-order bug:\*\* `ST\_Point(lng, lat)` vs `ST\_Point(lat, lng)` produced silently wrong coordinates when transforming between WGS84 and Web Mercator, causing every spatial join to fail with zero matches (no error, no warning). Diagnosed by manually comparing transformed output against known-good reference coordinates.



\## Status



Pipeline is live and collecting daily snapshots. Response-time analysis is pending real snowfall (Syracuse open-data shows "Not Serviced" uniformly during the off-season, as expected).

