import streamlit as st
import pandas as pd
import time
import re
from firebase_config import initialize_firebase

# Initialize Firebase
firestore_client = initialize_firebase()

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
    
    # Get all unique columns
    all_columns = set()
    for df in dfs:
        all_columns.update(df.columns)
    
    # Standardize column names
    column_mapping = standardize_columns(all_columns)
    
    # Rename columns in each DataFrame
    for i, df in enumerate(dfs):
        df.rename(columns=column_mapping, inplace=True)
    
    # Merge all DataFrames
    merged_df = pd.concat(dfs, ignore_index=True, sort=False)
    return merged_df

def main():
    st.title("✨ Firestore Data Merger ✨")
    
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

if __name__ == "__main__":
    main()
