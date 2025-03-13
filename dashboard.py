import streamlit as st
import pandas as pd
import time
from firebase_config import initialize_firebase

# Initialize Firebase
firestore_client = initialize_firebase()

def fetch_data(collection_name):
    """Fetch data from a Firestore collection."""
    try:
        docs = firestore_client.collection(collection_name).stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def merge_data(df1, df2):
    """Merge two DataFrames on common columns, aligning Q1-Q14 fields."""
    common_columns = list(set(df1.columns) & set(df2.columns))
    question_columns = [col for col in common_columns if any(f"Q{i}" in col for i in range(1, 15))]
    other_columns = list(set(common_columns) - set(question_columns))
    
    df1["Source_Collection"] = "Collection 1"
    df2["Source_Collection"] = "Collection 2"
    
    merged_df = pd.concat([df1, df2], ignore_index=True)
    return merged_df

def main():
    st.title("✨ Firestore Data Merger ✨")
    
    collections = firestore_client.collections()
    collection_names = [col.id for col in collections]
    
    if len(collection_names) < 2:
        st.warning("At least two collections are required for merging.")
        return
    
    col1, col2 = st.multiselect("📂 Select two collections to merge", collection_names, default=collection_names[:2])
    
    if len([col1, col2]) != 2:
        return
    
    df1 = fetch_data(col1)
    df2 = fetch_data(col2)
    
    if df1.empty or df2.empty:
        st.warning("⚠ One or both collections are empty.")
        return
    
    merged_df = merge_data(df1, df2)
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
