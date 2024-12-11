import pandas as pd
from email_analyzer import EmailAnalyzer

# Define evaluation pairs (query, expected thread id)
evaluation_pairs = [
    ("Thailand", [1003]),  # Assuming thread_id 1003 is related to Thailand
    ("Astros Tickets", [3337]),  # Assuming thread_id 3337 is for Astros Tickets
    ("Wolf -Reply", [1043]),  # Assuming thread_id 1043 is for Wolf -Reply
]

# Initialize the EmailAnalyzer
analyzer = EmailAnalyzer('email_thread_details.csv')

# Function to test evaluation pairs
def test_email_search():
    for query, expected_ids in evaluation_pairs:
        print(f"Testing query: '{query}'")
        results = analyzer.search_emails(query)
        result_ids = results['thread_id'].tolist()
        assert set(expected_ids).issubset(set(result_ids)), \
            f"Expected thread IDs {expected_ids} not found in results {result_ids}"
        print(f"Passed: Found expected thread IDs for query '{query}'.")

if __name__ == '__main__':
    test_email_search()
