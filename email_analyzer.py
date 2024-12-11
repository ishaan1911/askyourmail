import pandas as pd
import numpy as np
from typing import Union, List

class EmailAnalyzer:
    def __init__(self, data_path: str):
        """Initialize the EmailAnalyzer with a dataset path."""
        self.df = pd.read_csv(data_path)
        
    def search(self, query: str) -> pd.DataFrame:
        """
        Search through the email dataset based on the query.
        Returns matching results as a DataFrame.
        """
        # Convert all columns to string type for searching
        df_str = self.df.astype(str)
        
        # Search across all columns
        mask = df_str.apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        return self.df[mask]
    
    def get_statistics(self) -> dict:
        """Return basic statistics about the email dataset."""
        stats = {
            'total_emails': len(self.df),
            'columns': list(self.df.columns),
            'null_counts': self.df.isnull().sum().to_dict()
        }
        return stats
    
    def get_sample_emails(self, n: int = 10) -> pd.DataFrame:
        """Return a sample of n emails from the dataset."""
        sample = self.df.sample(n=n, random_state=42)
        # Save the sample to a CSV file
        sample.to_csv('selected_emails.csv', index=False)
        return sample
    
    def search_emails(self, query: str) -> pd.DataFrame:
        """Search for emails containing the query string."""
        # Convert all columns to string type for searching
        df_str = self.df.astype(str)
        # Search across all columns
        mask = df_str.apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        results = self.df[mask]
        # Save results to CSV
        results.to_csv('search_results.csv', index=False)
        return results

def main():
    # Initialize analyzer with the email dataset
    analyzer = EmailAnalyzer('email_thread_details.csv')
    
    # Get and display 10 random emails
    print("\n=== Sample of 10 Emails ===")
    sample_emails = analyzer.get_sample_emails(10)
    
    for idx, email in sample_emails.iterrows():
        print(f"\n------- Email {idx + 1} -------")
        print(f"Thread ID: {email['thread_id']}")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"To: {email['to']}")
        print(f"Timestamp: {email['timestamp']}")
        print(f"Body: {email['body'][:200]}{'...' if len(email['body']) > 200 else ''}")
        print("-" * 50)
    
    print("\nSelected emails have been saved to 'selected_emails.csv'")
    
    # Search for Thailand-related emails
    print("\n=== Emails Related to Thailand ===")
    thailand_emails = analyzer.search_emails('Thailand')
    
    if len(thailand_emails) == 0:
        print("No emails found related to Thailand.")
    else:
        for idx, email in thailand_emails.iterrows():
            print(f"\n------- Email {idx + 1} -------")
            print(f"Thread ID: {email['thread_id']}")
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"To: {email['to']}")
            print(f"Timestamp: {email['timestamp']}")
            print(f"Body: {email['body']}")
            print("-" * 50)
        
        print(f"\nFound {len(thailand_emails)} emails related to Thailand.")
        print("Results have been saved to 'search_results.csv'")

if __name__ == "__main__":
    main()
