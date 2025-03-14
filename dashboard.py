import streamlit as st
import pandas as pd
import time
import re
import plotly.express as px
from firebase_config import initialize_firebase

# Initialize Firebase
firestore_client = initialize_firebase()

@st.cache_data
def fetch_data(collection_name):
    """Fetch data from a Firestore collection."""
    try:
        docs = firestore_client.collection(collection_name).stream()
        data = [doc.to_dict() for doc in docs]
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if not df.empty:
            df["Source_Collection"] = collection_name  # Add collection identifier
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def standardize_columns(columns):
    """Standardize column names to group Q1-Q14 fields and other common columns."""
    column_mapping = {}
    for col in columns:
        match = re.search(r"Q(\d{1,2})", col, re.IGNORECASE)
        if match:
            column_mapping[col] = f"Q{match.group(1)}"
        else:
            column_mapping[col] = col
    return column_mapping

def merge_data(dfs):
    """Merge multiple DataFrames, aligning Q1-Q14 fields and common columns."""
    if not dfs:
        return pd.DataFrame()
    
    all_columns = set()
    for df in dfs:
        all_columns.update(df.columns)
    
    column_mapping = standardize_columns(all_columns)
    
    for i, df in enumerate(dfs):
        df.rename(columns=column_mapping, inplace=True)
    
    merged_df = pd.concat(dfs, ignore_index=True, sort=False)
    return merged_df

def plot_dashboard(df):
    """Create a well-structured dashboard with Plotly visualizations."""
    st.subheader("📊 Interactive Data Dashboard")
    
    numeric_columns = [col for col in df.columns if re.match(r"Q\d+", col)]
    
    if not numeric_columns:
        st.warning("No numeric fields found for visualization.")
        return
    
    # Trend Analysis
    with st.container():
        st.subheader("📈 Trend Analysis")
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["date"] = df["timestamp"].dt.date
            trend_df = df.groupby("date").size().reset_index(name="count")
            fig = px.line(trend_df, x="date", y="count", title="Response Trend Over Time", markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    # Response Distributions (Histograms)
    with st.container():
        st.subheader("📊 Response Distributions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if "Q4" in df.columns:
                fig = px.histogram(df, x="Q4", title="Distribution of Q4", nbins=10, color="Group", barmode="overlay")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if "Q8" in df.columns:
                q8_counts = df["Q8"].value_counts().reset_index()
                q8_counts.columns = ["Response", "Count"]
                fig = px.bar(q8_counts, x="Response", y="Count", title="Distribution of Q8", color="Response")
                st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            if "Q13" in df.columns:
                q13_counts = df["Q13"].value_counts().reset_index()
                q13_counts.columns = ["Level", "Count"]
                fig = px.bar(q13_counts, x="Level", y="Count", title="Distribution of Q13", color="Level")
                st.plotly_chart(fig, use_container_width=True)
    
    # User Engagement Metrics
    if "user_id" in df.columns and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        dau = df.groupby("date")["user_id"].nunique()
        repeat_users = df["user_id"].value_counts()
        repeat_user_rate = (repeat_users > 1).sum() / len(repeat_users)
        
        st.subheader("📊 User Engagement Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Daily Active Users (DAU)", dau.mean())
        with col2:
            st.metric("Repeat User Rate", f"{repeat_user_rate:.2%}")
        
        fig = px.line(x=dau.index, y=dau.values, title="DAU Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("✨ Firestore Data Analytics Dashboard ✨")
    
    collections = firestore_client.collections()
    collection_names = [col.id for col in collections]
    
    if not collection_names:
        st.warning("No collections found in Firestore.")
        return
    
    dfs = [fetch_data(col) for col in collection_names]
    
    if all(df.empty for df in dfs):
        st.warning("⚠ All collections are empty.")
        return
    
    merged_df = merge_data(dfs)
    st.markdown("**📊 Merged Data Preview:**")
    st.dataframe(merged_df, use_container_width=True)
    
    if not merged_df.empty:
        csv = merged_df.to_csv(index=False).encode("utf-8")
        if st.download_button("📥 Download Merged CSV", data=csv, file_name="merged_data.csv", mime="text/csv"):
            st.success("✅ Download started!")
            time.sleep(1)
            st.toast("🎉 File downloaded successfully!")
        
        plot_dashboard(merged_df)

if __name__ == "__main__":
    main()
