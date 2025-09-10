import pytest
import pandas as pd
import numpy as np
from numpy import nan


@pytest.fixture
def df():
    df = pd.read_csv('D:/ETL Testing - Python/duplicatecheck.csv')
    return df

# Test to check for duplicate records in the DataFrame
def test_duplicate_records(df):
    dupemp = df[df.duplicated()]
    assert len(dupemp) == 0, f"Test failed: {len(dupemp)} duplicate records found."
    dupemp.to_csv('D:/ETL Testing - Python/duplicate_emp.csv')
    print('Duplicate Record saved in file - Python/duplicate_emp.csv')


def test_unique_title_values(df):
    # List of titles we want to check
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
    

def test_title_value_counts(df):    # Get the counts of each unique title value
    title_counts = df['title'].value_counts()
    print("Title counts in DataFrame: \n")
    print(title_counts)
    print("\n")
    assert title_counts.sum() == len(df), f"Test failed: Expected {len(df)} total records, found {title_counts.sum()}."

