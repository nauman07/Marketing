import streamlit as st
import pandas as pd
from firebase_config import initialize_firebase

# Initialize Firebase
firestore_client = initialize_firebase()

def fetch_data(collection_name):
    try:
        docs = firestore_client.collection(collection_name).stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def main():
    st.title("Firestore Data Viewer")
    
    # Get all collection names
    collections = firestore_client.collections()
    collection_names = [col.id for col in collections]
    
    if not collection_names:
        st.warning("No collections found in Firestore.")
        return
    
    # Collection selection dropdown
    selected_collection = st.selectbox("Select a collection", collection_names)
    
    # Fetch data from selected collection
    df = fetch_data(selected_collection)
    
    if df.empty:
        st.warning("No data available in this collection.")
        return
    
    # Dynamic column filters
    filters = {}
    for col in df.columns:
        unique_values = df[col].dropna().unique().tolist()
        if len(unique_values) > 1 and len(unique_values) < 20:
            filters[col] = st.multiselect(f"Filter {col}", unique_values, default=unique_values)
        else:
            filters[col] = unique_values
    
    # Apply filters
    for col, values in filters.items():
        df = df[df[col].isin(values)]
    
    # Display table
    st.dataframe(df)
    
    # Download data as CSV
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{selected_collection}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
