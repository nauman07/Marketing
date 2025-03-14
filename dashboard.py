import streamlit as st
import pandas as pd
import time
import re
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
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
    
    all_columns = set()
    for df in dfs:
        all_columns.update(df.columns)
    
    column_mapping = standardize_columns(all_columns)
    
    for i, df in enumerate(dfs):
        df.rename(columns=column_mapping, inplace=True)
    
    merged_df = pd.concat(dfs, ignore_index=True, sort=False)
    return merged_df

def plot_dashboard(df):
    """Create a well-structured dashboard with multiple visualizations."""
    st.subheader("📊 Interactive Data Dashboard")
    
    # Separate the data into bias and control groups
    bias_group = df[df['Source_Collection'] == 'survey_bais']
    control_group = df[df['Source_Collection'] == 'survey_control']
    
    # Debugging: Print columns in the DataFrame
    st.write("Columns in the DataFrame:", df.columns.tolist())
    
    # 1. Bar Plot: Average Supplier Allocation
    st.subheader("📊 Average Supplier Allocation")
    suppliers = ['Supplier A: in %', 'Supplier B: in %', 'Supplier C: in %']
    
    # Check if supplier columns exist and are numeric
    valid_suppliers = [supplier for supplier in suppliers if supplier in df.columns and pd.api.types.is_numeric_dtype(df[supplier])]
    
    if not valid_suppliers:
        st.warning("No valid supplier data found for visualization.")
    else:
        bias_avgs = [bias_group[supplier].mean() for supplier in valid_suppliers]
        control_avgs = [control_group[supplier].mean() for supplier in valid_suppliers]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(valid_suppliers))
        width = 0.35
        
        # Plot bias group averages
        ax.bar([i - width/2 for i in x], bias_avgs, width, label='Bias Group', color='skyblue')
        # Plot control group averages
        ax.bar([i + width/2 for i in x], control_avgs, width, label='Control Group', color='lightcoral')
        
        ax.set_xlabel('Supplier')
        ax.set_ylabel('Average Percentage Allocation')
        ax.set_title('Average Percentage Allocation for Each Supplier in Bias vs Control Groups')
        ax.set_xticks(x)
        ax.set_xticklabels(valid_suppliers)
        ax.legend()
        
        st.pyplot(fig)
    
    # 2. Box Plot: Confidence Levels (Q2)
    st.subheader("📊 Distribution of Confidence Levels (Q2)")
    if 'Q2' in df.columns and pd.api.types.is_numeric_dtype(df['Q2']):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x='Source_Collection', y='Q2', data=df, palette="Set2", ax=ax)
        ax.set_xlabel('Group')
        ax.set_ylabel('Confidence Level (Q2)')
        ax.set_title('Distribution of Confidence Levels in Bias vs Control Groups')
        st.pyplot(fig)
    else:
        st.warning("Q2 data is missing or not numeric.")
    
    # 3. Histogram: Minimum Reliability Preferences (Q9)
    st.subheader("📊 Distribution of Minimum Reliability Preferences (Q9)")
    if 'Q9' in df.columns and pd.api.types.is_numeric_dtype(df['Q9']):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(bias_group['Q9'], kde=True, color='skyblue', label='Bias Group', ax=ax)
        sns.histplot(control_group['Q9'], kde=True, color='lightcoral', label='Control Group', ax=ax)
        ax.set_xlabel('Minimum Reliability Percentage (Q9)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Minimum Reliability Preferences')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Q9 data is missing or not numeric.")
    
    # 4. Histogram: Willingness to Invest (Q14)
    st.subheader("📊 Distribution of Willingness to Invest (Q14)")
    if 'Q14' in df.columns and pd.api.types.is_numeric_dtype(df['Q14']):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(bias_group['Q14'], kde=True, color='skyblue', label='Bias Group', ax=ax)
        sns.histplot(control_group['Q14'], kde=True, color='lightcoral', label='Control Group', ax=ax)
        ax.set_xlabel('Willingness to Invest (Q14)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Willingness to Invest in Quality Testing')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Q14 data is missing or not numeric.")
    
    # 5. Perform t-tests for each supplier
    st.subheader("📊 Statistical Tests: Supplier Allocation")
    if valid_suppliers:
        results = []
        
        for supplier in valid_suppliers:
            bias_data = bias_group[supplier].dropna()
            control_data = control_group[supplier].dropna()
            
            # Perform two-sample t-test
            t_stat, p_value = stats.ttest_ind(bias_data, control_data)
            results.append({
                "Supplier": supplier,
                "T-Statistic": t_stat,
                "P-Value": p_value,
                "Significance": "Significant" if p_value < 0.05 else "Not Significant"
            })
        
        # Display results in a table
        results_df = pd.DataFrame(results)
        st.table(results_df)
    else:
        st.warning("No valid supplier data found for statistical tests.")
    
    # 6. Chi-Square Test for Q8 and Q13
    st.subheader("📊 Chi-Square Test Results")
    
    if 'Q8' in df.columns and 'Q13' in df.columns:
        # Create a contingency table for Q8 and Group
        q8_contingency = pd.crosstab(df['Q8'], df['Source_Collection'])
        chi2_q8, p_q8, _, _ = stats.chi2_contingency(q8_contingency)
        
        # Create a contingency table for Q13 and Group
        q13_contingency = pd.crosstab(df['Q13'], df['Source_Collection'])
        chi2_q13, p_q13, _, _ = stats.chi2_contingency(q13_contingency)
        
        # Display Chi-Square Results
        chi2_results = [
            {"Variable": "Q8", "Chi-Square Statistic": chi2_q8, "P-Value": p_q8, "Significance": "Significant" if p_q8 < 0.05 else "Not Significant"},
            {"Variable": "Q13", "Chi-Square Statistic": chi2_q13, "P-Value": p_q13, "Significance": "Significant" if p_q13 < 0.05 else "Not Significant"}
        ]
        chi2_results_df = pd.DataFrame(chi2_results)
        st.table(chi2_results_df)
    else:
        st.warning("Q8 or Q13 data is missing.")

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
