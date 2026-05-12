# =====================================================
# Funded 2026 - Analysis File
# Client: VC Advisory Partners LLP
# Analyst: Remsha Ansari
# Deadline: 12-May-2026 6:00 PM
# =====================================================

import pandas as pd
import numpy as np
import re

# ==================== 1. DATA LOADING & CLEANING ====================
print("Loading and cleaning data...")

# Load CSV
df = pd.read_csv('data/funding_data_2026.csv')

# --- Clean Funding Amount ---
# Remove $, commas, convert blanks to NaN, then fill with 0 for "Undisclosed"
df['Funding Amount (USD)'] = df['Funding Amount (USD)'].astype(str).str.replace('$', '').str.replace(',', '')
df['Funding Amount (USD)'] = pd.to_numeric(df['Funding Amount (USD)'], errors='coerce')
df['Is_Undisclosed'] = df['Funding Amount (USD)'].isna()
df['Funding Amount (USD)'] = df['Funding Amount (USD)'].fillna(0)

# --- Clean Funding Type ---
df['Funding Type'] = df['Funding Type'].fillna('Unknown')

# --- Clean Date ---
# Convert 'Feb-26' to proper date. Assume 2026
df['Last Funding Date'] = pd.to_datetime(df['Last Funding Date'], format='%b-%y')
df['Month'] = df['Last Funding Date'].dt.strftime('%b-2026')
df['Month_Num'] = df['Last Funding Date'].dt.month

# --- Clean Industry ---
# Use FIRST sector only to avoid double counting
df['Primary Industry'] = df['Industry'].str.split(',').str[0].str.strip()
df['Industry_Count'] = df['Industry'].str.count(',') + 1

# --- Create Stage Groups ---
def get_stage_group(stage):
    if stage in ['Pre-Seed', 'Seed']:
        return 'Early Stage'
    elif stage in ['Series A', 'Series B', 'Series C']:
        return 'Growth Stage'
    elif stage in ['Series D', 'Series E', 'Series F']:
        return 'Late Stage'
    elif stage == 'Private Equity':
        return 'Private Equity'
    else:
        return 'Other/Unknown'

df['Stage_Group'] = df['Funding Type'].apply(get_stage_group)

print("Data cleaning complete. Shape:", df.shape)
print("-" * 50)

# ==================== 2. BUSINESS QUESTIONS ANALYSIS ====================

# SECTION A: HIGH-LEVEL KPIs
print("\n=== SECTION A: HIGH-LEVEL KPIs ===")

# Q1: Total funding raised Jan-Feb 2026
# Exclude undisclosed deals from sum
q1_total_funding = df['Funding Amount (USD)'].sum()
print(f"Q1. Total Funding Jan-Feb 2026: ${q1_total_funding/1e6:.1f}M")

# Q2: Total deals + Average deal size
q2_total_deals = len(df)
q2_avg_deal = df[df['Funding Amount (USD)'] > 0]['Funding Amount (USD)'].mean()
print(f"Q2. Total Deals: {q2_total_deals}")
print(f" Avg Deal Size: ${q2_avg_deal/1e6:.2f}M")

# Q3: Top 5 startups by funding
q3_top5 = df.nlargest(5, 'Funding Amount (USD)')[['Name', 'Funding Amount (USD)', 'Primary Industry', 'Funding Type']]
print(f"\nQ3. Top 5 Startups by Funding:")
print(q3_top5.to_string(index=False))

# SECTION B: SECTOR & STAGE TRENDS
print("\n=== SECTION B: SECTOR & STAGE TRENDS ===")

# Q4: Top 5 sectors by funding + deal count
q4_top_sectors = df.groupby('Primary Industry').agg({
    'Funding Amount (USD)': 'sum',
    'Name': 'count'
}).rename(columns={'Name': 'Deal Count'}).nlargest(5, 'Funding Amount (USD)')
print(f"\nQ4. Top 5 Sectors by Funding:")
print(q4_top_sectors)

# Q5: % funding by Stage Group
q5_stage_pct = df.groupby('Stage_Group')['Funding Amount (USD)'].sum() / q1_total_funding * 100
print(f"\nQ5. Funding % by Stage:")
print(q5_stage_pct.round(1))

# Q6: Sector with highest Pre-Seed deals
q6_preseed = df[df['Funding Type'] == 'Pre-Seed']['Primary Industry'].value_counts().head(1)
print(f"\nQ6. Sector with Most Pre-Seed Deals: {q6_preseed.index[0]} - {q6_preseed.values[0]} deals")

# SECTION C: TIME & TYPE ANALYSIS
print("\n=== SECTION C: TIME & TYPE ANALYSIS ===")

# Q7: Jan vs Feb funding comparison
q7_month = df.groupby('Month')['Funding Amount (USD)'].sum().sort_index()
jan_funding = q7_month.get('Jan-2026', 0)
feb_funding = q7_month.get('Feb-2026', 0)
q7_growth = ((feb_funding - jan_funding) / jan_funding * 100) if jan_funding > 0 else 0
print(f"\nQ7. Jan 2026: ${jan_funding/1e6:.1f}M | Feb 2026: ${feb_funding/1e6:.1f}M")
print(f" Growth: {q7_growth:.1f}%")

# Q8: Breakdown of all Funding Types
q8_types = df['Funding Type'].value_counts()
print(f"\nQ8. Funding Type Breakdown:")
print(q8_types)

# Q9: Unicorn Potential deals >$20M
q9_unicorn = df[df['Funding Amount (USD)'] > 20_000_000][['Name', 'Funding Amount (USD)', 'Primary Industry']]
print(f"\nQ9. Unicorn Potential Deals >$20M: {len(q9_unicorn)} deals")
print(q9_unicorn.to_string(index=False))

# SECTION D: ADVANCED INSIGHTS
print("\n=== SECTION D: ADVANCED INSIGHTS ===")

# Q10: Top Industry COMBINATION for multi-industry startups
multi_industry = df[df['Industry_Count'] > 1].copy()
q10_combo = multi_industry.groupby('Industry')['Funding Amount (USD)'].sum().nlargest(5)
print(f"\nQ10. Top Industry Combinations by Funding:")
print(q10_combo)

# Q11: % of Undisclosed deals
q11_undisclosed_pct = df['Is_Undisclosed'].sum() / len(df) * 100
print(f"\nQ11. % Undisclosed Deals: {q11_undisclosed_pct:.1f}%")

# Q12: Funding Type with highest avg deal size
q12_avg_by_type = df[df['Funding Amount (USD)'] > 0].groupby('Funding Type')['Funding Amount (USD)'].mean().nlargest(1)
print(f"\nQ12. Funding Type with Highest Avg Deal: {q12_avg_by_type.index[0]} - ${q12_avg_by_type.values[0]/1e6:.2f}M")

# ==================== 3. EXPORT CLEANED DATA ====================
df.to_csv('data/funding_data_2026_cleaned.csv', index=False)
print("\n" + "=" * 50)
print("Analysis Complete! Cleaned data saved to: data/funding_data_2026_cleaned.csv")
print("Run this file first, then run app.py for dashboard")
print("=" * 50)

# ==================== 4. SUMMARY FOR README ====================
insights = f"""
KEY INSIGHTS FOR BOARD:
1. Total ${q1_total_funding/1e9:.2f}B raised across {q2_total_deals} deals in 2 months. Avg deal: ${q2_avg_deal/1e6:.1f}M
2. {q5_stage_pct.get('Early Stage', 0):.1f}% funding went to Early Stage. {q6_preseed.index[0]} leads in new startup formation
3. {q11_undisclosed_pct:.1f}% deals are undisclosed - transparency issue. {q7_growth:.1f}% {'growth' if q7_growth>0 else 'decline'} from Jan to Feb
"""
print(insights)

with open('insights.txt', 'w') as f:
    f.write(insights)