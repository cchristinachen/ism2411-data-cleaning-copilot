"""
PURPOSE: Clean a messy sales CSV and save a cleaned version for analysis.
WHY: Standardized, reproducible cleaning that recruiters can run.

STEPS: 
1. Load raw data 
2. Standardize column names
3. Strip whitespace from product/category text fields
4. Handle missing values consistently 
5. Remove negative price/quantity 
6. Save to data/processed/sales_data_clean.csv

"""
import os
import pandas as pd

"""
TASK: Load a CSV into a DataFrame from a given path.

STEPS:
1. Read the CSV using pandas.read_csv.
2. Do not change dtypes yet; just return the raw DataFrame.

OUTPUT:
- pandas.DataFrame containing the raw data.
"""
# WHY: Start with the raw data exactly as stored on file. 
def load_data(file_path: str):
    return pd.read_csv(file_path)
    
"""
TASK: Standardize column names so they are easy to work with.

STEPS:
1. Lowercase all names.
2. Strip surrounding whitespace.
3. Replace internal spaces with underscores.
4. Replace '/' and '-' with underscores (common in messy headers).
5. Collapse any double underscores created by replacements.

OUTPUT:
- New DataFrame with standardized .columns (values themselves unchanged).
"""
# WHY: Clean column names make the rest of the script easy to work with. 
def clean_column_names(df):
    new_cols = []
    for c in df.columns:
        name = str(c).strip().lower()
        name = name.replace(" ", "_").replace("/", "_").replace("-", "_")
        while "__" in name:
            name = name.replace("__", "_")
        new_cols.append(name)
    df = df.copy()
    df.columns = new_cols
    return df

"""
TASK: Strip leading/trailing whitespace from product and category text columns.
STEPS:
1. Identify any columns whose name contains "product" or "category".
2. Convert to string and .str.strip() to remove extra spaces.
OUTPUT: DataFrame with trimmed text fields for product/category.
"""
# WHY: Extra spaces cause duplicate-looking values and broken filters.
def strip_product_and_category(df):
    df = df.copy()
    target_cols = [c for c in df.columns if ("product" in c) or ("category" in c)]
    for col in target_cols:
        df[col] = df[col].astype(str).str.strip()
    return df
  
"""
TASK: Handle missing values for price and quantity CONSISTENTLY.

STEPS:
1. First, coerce 'price' and 'quantity' to numeric (invalid -> NaN).
2. Drop rows where price is NaN OR quantity is NaN.
3. Return the cleaned DataFrame.

OUTPUT:
- DataFrame with no missing price/quantity.
"""
# WHY: Calculations require valid numbers; we apply one clear rule across the file.
def handle_missing_values(df):
    df = df.copy()
    for col in ("price", "quantity"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    required_cols = [c for c in ("price", "quantity") if c in df.columns]
    if required_cols:
        df = df.dropna(subset=required_cols)
    return df

"""
TASK: Remove clearly invalid rows (negative price or negative quantity).

STEPS:
1. Ensure numeric types for 'price' and 'quantity'.
2. Filter out rows where price < 0 or quantity < 0 (data entry errors).
3. Return the filtered DataFrame.

OUTPUT:
- DataFrame containing only valid non-negative price/quantity rows.
"""
# WHY: Negative values here are data entry errors and should not be analyzed.
def remove_invalid_rows(df):
    df = df.copy()  
    for col in ("price", "quantity"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "price" in df.columns:
        df = df[df["price"] >= 0]
    if "quantity" in df.columns:
        df = df[df["quantity"] >= 0]
    return df

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"
    
    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = strip_product_and_category(df_clean) 
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
