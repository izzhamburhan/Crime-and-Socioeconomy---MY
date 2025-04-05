import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for better visualizations
plt.style.use('seaborn')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = [12, 6]

# 1. Load and preprocess the data
def load_data():
    # Load datasets
    crime_df = pd.read_csv('data/crime_district.csv')
    income_df = pd.read_csv('data/hh_income_state.csv')
    poverty_df = pd.read_csv('data/hh_poverty_state.csv')
    labor_df = pd.read_csv('data/lfs_state_sex.csv')
    
    # Convert dates to datetime
    for df in [crime_df, income_df, poverty_df, labor_df]:
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
    
    return crime_df, income_df, poverty_df, labor_df

# 2. Analyze crime trends
def analyze_crime(crime_df):
    # Group crimes by year and category
    crime_yearly = crime_df.groupby(['year', 'category'])['crimes'].sum().reset_index()
    
    # Plot crime trends
    plt.figure(figsize=(15, 8))
    for category in crime_yearly['category'].unique():
        data = crime_yearly[crime_yearly['category'] == category]
        plt.plot(data['year'], data['crimes'], marker='o', label=category)
    
    plt.title('Crime Trends by Category (2016-2023)')
    plt.xlabel('Year')
    plt.ylabel('Number of Crimes')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/crime_trends.png')
    plt.close()
    
    # Calculate year-over-year change
    yearly_total = crime_df.groupby('year')['crimes'].sum()
    yoy_change = yearly_total.pct_change() * 100
    return yoy_change

# 3. Analyze income trends
def analyze_income(income_df):
    # Plot income trends
    plt.figure(figsize=(15, 8))
    for state in income_df['state'].unique():
        data = income_df[income_df['state'] == state]
        plt.plot(data['year'], data['income_mean'], label=state)
    
    plt.title('Mean Household Income Trends by State')
    plt.xlabel('Year')
    plt.ylabel('Mean Income')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/income_trends.png')
    plt.close()
    
    # Calculate income growth
    recent_years = income_df[income_df['year'] >= 2010]
    income_growth = recent_years.groupby('state')['income_mean'].pct_change().mul(100)
    return income_growth

# 4. Analyze poverty trends
def analyze_poverty(poverty_df):
    # Plot poverty trends
    plt.figure(figsize=(15, 8))
    for state in poverty_df['state'].unique():
        data = poverty_df[poverty_df['state'] == state]
        plt.plot(data['year'], data['poverty_absolute'], label=state)
    
    plt.title('Absolute Poverty Rate Trends by State')
    plt.xlabel('Year')
    plt.ylabel('Absolute Poverty Rate (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/poverty_trends.png')
    plt.close()
    
    # Calculate poverty reduction
    poverty_change = poverty_df.groupby('state').agg({
        'poverty_absolute': ['first', 'last']
    }).round(2)
    poverty_change.columns = ['Initial Rate', 'Final Rate']
    poverty_change['Reduction'] = poverty_change['Initial Rate'] - poverty_change['Final Rate']
    return poverty_change

# 5. Analyze labor force trends
def analyze_labor(labor_df):
    # Plot unemployment trends
    plt.figure(figsize=(15, 8))
    for state in labor_df['state'].unique():
        data = labor_df[labor_df['state'] == state]
        plt.plot(data['year'], data['u_rate'], label=state)
    
    plt.title('Unemployment Rate Trends by State')
    plt.xlabel('Year')
    plt.ylabel('Unemployment Rate (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/unemployment_trends.png')
    plt.close()
    
    # Calculate average unemployment rates
    recent_unemployment = labor_df[labor_df['year'] >= 2010].groupby('state')['u_rate'].mean().round(2)
    return recent_unemployment

# 6. Analyze correlations between crime and socioeconomic factors
def analyze_correlations(crime_df, income_df, poverty_df, labor_df):
    # Prepare data for correlation analysis
    # Aggregate crime data by year and state
    crime_yearly = crime_df.groupby(['year', 'state'])['crimes'].sum().reset_index()
    
    # Merge datasets
    merged_data = crime_yearly.merge(income_df[['year', 'state', 'income_mean']], 
                                   on=['year', 'state'], how='left')
    merged_data = merged_data.merge(poverty_df[['year', 'state', 'poverty_absolute']], 
                                  on=['year', 'state'], how='left')
    merged_data = merged_data.merge(labor_df[['year', 'state', 'u_rate']], 
                                  on=['year', 'state'], how='left')
    
    # Calculate correlations
    correlations = merged_data[['crimes', 'income_mean', 'poverty_absolute', 'u_rate']].corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlations, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation between Crime and Socioeconomic Factors')
    plt.savefig('results/correlations.png')
    plt.close()
    
    return correlations

def main():
    # Create results directory if it doesn't exist
    import os
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Load data
    crime_df, income_df, poverty_df, labor_df = load_data()
    
    # Run analyses
    print("Analyzing crime trends...")
    crime_changes = analyze_crime(crime_df)
    print("\nYear-over-year crime changes:")
    print(crime_changes)
    
    print("\nAnalyzing income trends...")
    income_growth = analyze_income(income_df)
    print("\nIncome growth rates:")
    print(income_growth)
    
    print("\nAnalyzing poverty trends...")
    poverty_reduction = analyze_poverty(poverty_df)
    print("\nPoverty reduction by state:")
    print(poverty_reduction)
    
    print("\nAnalyzing labor force trends...")
    unemployment_rates = analyze_labor(labor_df)
    print("\nAverage unemployment rates:")
    print(unemployment_rates)
    
    print("\nAnalyzing correlations...")
    correlations = analyze_correlations(crime_df, income_df, poverty_df, labor_df)
    print("\nCorrelations between factors:")
    print(correlations)
    
    print("\nAnalysis complete! Results have been saved to the 'results' directory.")

if __name__ == "__main__":
    main() 