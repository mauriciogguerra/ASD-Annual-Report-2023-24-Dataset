import pandas as pd
import matplotlib.pyplot as plt
import os

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE, "ASD-Annual-Report-2023-24-Dataset-23-24.csv")
IMAGES_DIR = os.path.join(BASE, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df

def monthly_incidents(df):
    # Rows filtration
    m = df[df['subcategory'] == 'By month'].copy()
    if m.empty:
        print("No monthly data found in dataset.")
        return None
    m['month'] = m['metric'].str.extract(r'\((\d{4}-\d{2})\)')
    m['count'] = pd.to_numeric(m['value'], errors='coerce')
    m = m.sort_values('month')
    # THis is the plot
    plt.figure(figsize=(10,4))
    plt.plot(m['month'], m['count'], marker='o')
    plt.title('Monthly incidents (ASD responses) — FY2023–24')
    plt.xlabel('Month')
    plt.ylabel('Incidents')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'monthly_incidents.png'))
    print("Saved monthly_incidents.png")
    return m

def incident_sectors(df):
    s = df[(df['category']=='Sectors') & (df['subcategory'].str.contains('Top reporting'))].copy()
    return s

def business_costs(df):
    b = df[(df['category']=='Business Impact') & (df['metric'].str.contains('business|Business', case=False))].copy()
    return b

def main():
    df = load_data()
    print("Loaded dataset with", len(df), "rows")
    m = monthly_incidents(df)
    s = incident_sectors(df)
    if s is not None and not s.empty:
        print("\nTop reporting sectors (sample):")
        print(s[['metric','value','unit']])
    b = business_costs(df)
    if b is not None and not b.empty:
        print("\nBusiness impact rows:")
        print(b[['metric','value','unit','change_vs_prev_year']])

    # Answers
    try:
        with open(os.path.join(BASE, 'Questions-and-Answers-for-ASD-2023-24-Dataset-Analysis.txt'),'r') as f:
            print('\n--- QUESTIONS & ANSWERS ---\n')
            print(f.read())
    except Exception as e:
        pass

if __name__ == '__main__':
    main()
