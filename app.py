import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(page_title="Syracuse Winter Operations Equity", layout="wide")

st.title("Syracuse Winter Operations Equity Dashboard")
st.caption("Snowplow priority classification and 311 complaint patterns by neighborhood")

con = duckdb.connect("syracuse_snow.duckdb", read_only=True)
con.execute("INSTALL spatial")
con.execute("LOAD spatial")

df = con.execute("SELECT * FROM neighborhood_equity_summary").df()

col1, col2, col3 = st.columns(3)
col1.metric("Neighborhoods analyzed", len(df))
col2.metric("Total complaints (2021-present)", int(df["total_complaints"].sum()))
col3.metric("Avg. % Priority 2 streets", f"{df['pct_priority_2'].mean():.1f}%")

st.subheader("Priority 2 (lower priority) street share by neighborhood")
fig1 = px.bar(
    df.sort_values("pct_priority_2", ascending=True),
    x="pct_priority_2",
    y="neighborhood_name",
    orientation="h",
    labels={"pct_priority_2": "% Priority 2 Streets", "neighborhood_name": "Neighborhood"},
    height=800,
)
st.plotly_chart(fig1, width='stretch')

st.subheader("Complaints per road segment by neighborhood")
fig2 = px.bar(
    df.sort_values("complaints_per_segment", ascending=True),
    x="complaints_per_segment",
    y="neighborhood_name",
    orientation="h",
    labels={"complaints_per_segment": "Complaints per Segment", "neighborhood_name": "Neighborhood"},
    height=800,
    color_discrete_sequence=["#e07b39"],
)
st.plotly_chart(fig2, width='stretch')

st.subheader("Full data table")
st.dataframe(df, width='stretch')

st.caption("Data: City of Syracuse Open Data Portal. Response-time analysis pending real winter snowfall data.")