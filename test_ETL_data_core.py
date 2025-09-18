import pytest
import pandas as pd
import pyodbc
import numpy as np
from numpy import nan


@pytest.fixture
def df():
    df = pd.read_csv('D:/ETL Testing - Python/duplicatecheck.csv')
    return df
@pytest.fixture
def target_db_ordersales():
    odf = pd.read_csv('D:/ETL Testing - Python/order_details.csv')
    odf['productSales'] = odf['unitPrice'] * odf['quantity']
    return odf
@pytest.fixture
def source_db_ordersales():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Use the appropriate driver version
        "SERVER=DESKTOP-77LK4FJ;"                 # Replace with your server name (e.g., "localhost" or ".\SQLEXPRESS")
        "DATABASE=northwind;"             # Replace with your database name
        "Trusted_Connection=yes;"                  # This enables Windows Authentication
        "Encrypt=yes;"                             # Enable encryption
        "TrustServerCertificate=yes;"              # Trust the certificate
    )
    conn = pyodbc.connect(conn_str)
    query = """
        SELECT productID as pid, Round(sum(unitPrice * quantity),2) as totalSales
        FROM [northwind].[dbo].[order_details]
        GROUP BY productID
    """
    source_db_ordersales = pd.read_sql(query, conn)
    conn.close()  
    return source_db_ordersales  

# Test1: Test to check for duplicate records in the DataFrame
def test_duplicate_records(df):
    dupemp = df[df.duplicated()]
    assert len(dupemp) == 0, f"Test failed: {len(dupemp)} duplicate records found."
    dupemp.to_csv('D:/ETL Testing - Python/duplicate_emp.csv')
    print('Duplicate Record saved in file - Python/duplicate_emp.csv')

# Test2: List of titles we want to check for uniqueness
def test_unique_title_values(df):
    titles_to_check = [
    'Vice President Sales',
    'Sales Representative',
    'Sales Manager',
    'Inside Sales Coordinator']

    # Check if all titles in the list are present in the 'title' column
    for title in titles_to_check:
        assert title in df['title'].values, f"Test failed: Title '{title}' not found in 'title' column."
    # Check the number of unique titles in the 'title' column   
        unique_titles = df['title'].unique()
        print("Unique titles in DataFrame:")
        print(*unique_titles, sep='\n')
        print("\n")
        assert len(unique_titles) == 4, f"Test failed: Expected 5 unique title values, found {unique_titles}."

# Test3: Get the counts of each unique title value
def test_title_value_counts(df):
    title_counts = df['title'].value_counts()
    print("Title counts in DataFrame: \n")
    print(title_counts)
    print("\n")
    assert title_counts.sum() == len(df), f"Test failed: Expected {len(df)} total records, found {title_counts.sum()}."

# Test4: compare Productwise total sales amount between source and target
def test_productwise_sales_amount(target_db_ordersales, source_db_ordersales):
    # Round the calculated product sales to 2 decimal places
    target_db_ordersales['productSales'] = target_db_ordersales['productSales'].round(2)
    
    # Calculate total sales per product
    product_sales = target_db_ordersales.groupby('productID')['productSales'].sum().round(2).reset_index()
    print("Target DB - Productwise total sales amount:\n")
    print(product_sales)
    print("\nSource DB - Productwise total sales amount:\n")
    print(source_db_ordersales)
    
    assert not product_sales.empty, "Test failed: No sales data found in target."
    assert not source_db_ordersales.empty, "Test failed: No sales data found in source."
    
    # Merge and compare with a small tolerance for floating-point differences
    merged_sales = pd.merge(product_sales, source_db_ordersales, left_on='productID', right_on='pid', how='inner')
    # Allow for a small difference (0.01) to account for rounding
    discrepancies = merged_sales[abs(merged_sales['productSales'] - merged_sales['totalSales']) > 0.01]
    
    if not discrepancies.empty:
        print("\nDetailed Discrepancies Report:")
        for _, row in discrepancies.iterrows():
            print(f"\nProduct ID: {row['productID']}")
            print(f"Target DB Amount: {row['productSales']:.2f}")
            print(f"Source DB Amount: {row['totalSales']:.2f}")
            print(f"Difference: {(row['productSales'] - row['totalSales']):.2f}")
    
    assert discrepancies.empty, f"Test failed: Significant discrepancies found in product sales amounts"