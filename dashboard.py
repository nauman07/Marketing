import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import chi2_contingency

# Sample Data (Replace this with your actual data)
def generate_sample_data():
    data = {
        "Q8": np.random.choice(["Yes", "No"], 100, p=[0.6, 0.4]),
        "Q13": np.random.choice(["Low", "Medium", "High"], 100, p=[0.3, 0.5, 0.2]),
        "Q4": np.random.randint(1, 10, 100),
        "Group": np.random.choice(["Bias Group", "Control Group"], 100),
    }
    return pd.DataFrame(data)

# Load Data
df = generate_sample_data()

# Title
st.title("📊 Concise Data Dashboard")

# Layout for Parallel Graphs
st.subheader("Parallel Visualizations")

# Create columns for parallel graphs
col1, col2, col3 = st.columns(3)

# Histogram for Q4
with col1:
    st.markdown("**Histogram: Q4**")
    fig = px.histogram(df, x="Q4", nbins=10, color="Group", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

# Bar Plot for Q8
with col2:
    st.markdown("**Bar Plot: Q8**")
    q8_counts = df["Q8"].value_counts().reset_index()
    q8_counts.columns = ["Response", "Count"]
    fig = px.bar(q8_counts, x="Response", y="Count", color="Response")
    st.plotly_chart(fig, use_container_width=True)

# Bar Plot for Q13
with col3:
    st.markdown("**Bar Plot: Q13**")
    q13_counts = df["Q13"].value_counts().reset_index()
    q13_counts.columns = ["Level", "Count"]
    fig = px.bar(q13_counts, x="Level", y="Count", color="Level")
    st.plotly_chart(fig, use_container_width=True)

# Trend Analysis (Over Time)
st.subheader("Trend Analysis")
df["Date"] = pd.date_range(start="2023-01-01", periods=len(df), freq="D")
trend_df = df.groupby(["Date", "Group"]).size().reset_index(name="Count")
fig = px.line(trend_df, x="Date", y="Count", color="Group", title="Response Trend Over Time")
st.plotly_chart(fig, use_container_width=True)

# Chi-Square Test for Q8 and Q13
st.subheader("Chi-Square Test Results")

# Create a contingency table for Q8 and Group
q8_contingency = pd.crosstab(df["Q8"], df["Group"])
chi2_q8, p_q8, _, _ = chi2_contingency(q8_contingency)

# Create a contingency table for Q13 and Group
q13_contingency = pd.crosstab(df["Q13"], df["Group"])
chi2_q13, p_q13, _, _ = chi2_contingency(q13_contingency)

# Display Chi-Square Results
st.markdown("**Chi-Square Test for Q8 (Yes/No) vs Group**")
st.write(f"Chi2 Statistic: {chi2_q8:.2f}, p-value: {p_q8:.4f}")
st.markdown("**Chi-Square Test for Q13 (Low/Medium/High) vs Group**")
st.write(f"Chi2 Statistic: {chi2_q13:.2f}, p-value: {p_q13:.4f}")

# Interpretation
st.markdown("**Interpretation:**")
st.write("- A p-value < 0.05 indicates a significant association between the variables.")
st.write(f"- Q8 vs Group: {'Significant' if p_q8 < 0.05 else 'Not Significant'}")
st.write(f"- Q13 vs Group: {'Significant' if p_q13 < 0.05 else 'Not Significant'}")

# Download Data
st.subheader("Download Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name="data.csv", mime="text/csv")
