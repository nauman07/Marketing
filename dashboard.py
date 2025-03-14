import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Load the data using Streamlit's file uploader
def load_data():
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        st.warning("Please upload a CSV file.")
        return None

# Separate the data into bias and control groups
def separate_groups(data):
    bias_group = data[data['Source_Collection'] == 'survey_bais']
    control_group = data[data['Source_Collection'] == 'survey_control']
    return bias_group, control_group

# Set the aesthetic style of the plots
sns.set(style="whitegrid", palette="pastel")

# Main function for the Streamlit app
def main():
    st.title("📊 Real-Time Data Analysis Dashboard")
    
    # Load data
    data = load_data()
    
    if data is not None:
        # Separate into bias and control groups
        bias_group, control_group = separate_groups(data)
        
        # Display raw data
        st.subheader("📂 Raw Data Preview")
        st.write(data.head())
        
        # 1. Bar Plot: Average Supplier Allocation
        st.subheader("📊 Average Supplier Allocation")
        suppliers = ['Supplier A: in %', 'Supplier B: in %', 'Supplier C: in %']
        bias_avgs = [bias_group[supplier].mean() for supplier in suppliers]
        control_avgs = [control_group[supplier].mean() for supplier in suppliers]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(suppliers))
        width = 0.35
        
        # Plot bias group averages
        ax.bar([i - width/2 for i in x], bias_avgs, width, label='Bias Group', color='skyblue')
        # Plot control group averages
        ax.bar([i + width/2 for i in x], control_avgs, width, label='Control Group', color='lightcoral')
        
        ax.set_xlabel('Supplier')
        ax.set_ylabel('Average Percentage Allocation')
        ax.set_title('Average Percentage Allocation for Each Supplier in Bias vs Control Groups')
        ax.set_xticks(x)
        ax.set_xticklabels(suppliers)
        ax.legend()
        
        st.pyplot(fig)
        
        # 2. Box Plot: Confidence Levels (Q2)
        st.subheader("📊 Distribution of Confidence Levels (Q2)")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x='Source_Collection', y='Q2', data=data, palette="Set2", ax=ax)
        ax.set_xlabel('Group')
        ax.set_ylabel('Confidence Level (Q2)')
        ax.set_title('Distribution of Confidence Levels in Bias vs Control Groups')
        st.pyplot(fig)
        
        # 3. Histogram: Minimum Reliability Preferences (Q9)
        st.subheader("📊 Distribution of Minimum Reliability Preferences (Q9)")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(bias_group['Q9'], kde=True, color='skyblue', label='Bias Group', ax=ax)
        sns.histplot(control_group['Q9'], kde=True, color='lightcoral', label='Control Group', ax=ax)
        ax.set_xlabel('Minimum Reliability Percentage (Q9)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Minimum Reliability Preferences')
        ax.legend()
        st.pyplot(fig)
        
        # 4. Histogram: Willingness to Invest (Q14)
        st.subheader("📊 Distribution of Willingness to Invest (Q14)")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(bias_group['Q14'], kde=True, color='skyblue', label='Bias Group', ax=ax)
        sns.histplot(control_group['Q14'], kde=True, color='lightcoral', label='Control Group', ax=ax)
        ax.set_xlabel('Willingness to Invest (Q14)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Willingness to Invest in Quality Testing')
        ax.legend()
        st.pyplot(fig)
        
        # 5. Perform t-tests for each supplier
        st.subheader("📊 Statistical Tests: Supplier Allocation")
        suppliers = ['Supplier A: in %', 'Supplier B: in %', 'Supplier C: in %']
        results = []
        
        for supplier in suppliers:
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
        
        # 6. Chi-Square Test for Q8 and Q13
        st.subheader("📊 Chi-Square Test Results")
        
        # Create a contingency table for Q8 and Group
        q8_contingency = pd.crosstab(data['Q8'], data['Source_Collection'])
        chi2_q8, p_q8, _, _ = stats.chi2_contingency(q8_contingency)
        
        # Create a contingency table for Q13 and Group
        q13_contingency = pd.crosstab(data['Q13'], data['Source_Collection'])
        chi2_q13, p_q13, _, _ = stats.chi2_contingency(q13_contingency)
        
        # Display Chi-Square Results
        chi2_results = [
            {"Variable": "Q8", "Chi-Square Statistic": chi2_q8, "P-Value": p_q8, "Significance": "Significant" if p_q8 < 0.05 else "Not Significant"},
            {"Variable": "Q13", "Chi-Square Statistic": chi2_q13, "P-Value": p_q13, "Significance": "Significant" if p_q13 < 0.05 else "Not Significant"}
        ]
        chi2_results_df = pd.DataFrame(chi2_results)
        st.table(chi2_results_df)

# Run the app
if __name__ == "__main__":
    main()
