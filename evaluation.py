import json
import numpy as np
from typing import List, Dict, Any
import math
from embeddings import generate_email_embeddings
from retrieval import retrieve_emails

# Example function to validate an email
def validate_email(email):
    # Check if 'body' key exists in the email
    if 'body' not in email:
        print(f"Skipping email {email['thread_id']} because it doesn't have 'body' key.")
        return None
    return email

# Function to evaluate (process) the emails
def evaluate_emails(emails):
    # Loop through emails to validate
    for email in emails:
        valid_email = validate_email(email)
        if valid_email is not None:
            # Proceed with evaluation or processing
            print(f"Evaluating email with subject: {valid_email['subject']}")
            # Perform further evaluation tasks here, like extracting content, sentiment analysis, etc.

def dcg_at_k(relevances: List[float], k: int) -> float:
    """Calculate DCG@k for a single query"""
    dcg = 0
    for i in range(min(len(relevances), k)):
        dcg += (2 ** relevances[i] - 1) / math.log2(i + 2)
    return dcg

def ndcg_at_k(relevances: List[float], ideal_relevances: List[float], k: int) -> float:
    """Calculate NDCG@k for a single query"""
    dcg = dcg_at_k(relevances, k)
    idcg = dcg_at_k(sorted(ideal_relevances, reverse=True), k)
    return dcg / idcg if idcg > 0 else 0.0

def precision_at_k(relevances: List[float], k: int) -> float:
    """Calculate Precision@k"""
    if k == 0:
        return 0.0
    relevances = [1 if r > 0 else 0 for r in relevances[:k]]
    return sum(relevances) / k

def recall_at_k(relevances: List[float], total_relevant: int, k: int) -> float:
    """Calculate Recall@k"""
    if total_relevant == 0:
        return 0.0
    relevances = [1 if r > 0 else 0 for r in relevances[:k]]
    return sum(relevances) / total_relevant

class EmailEvaluator:
    def __init__(self, emails: List[Dict[str, Any]]):
        """
        Initialize evaluator with email dataset
        
        Args:
            emails: List of email dictionaries
        """
        self.emails = emails
        # Generate embeddings for all emails
        self.email_embeddings = {}
        for email in emails:
            embedding = generate_email_embeddings(email)
            if embedding is not None:
                self.email_embeddings[email['thread_id']] = embedding
        
        # Test cases: (query, relevant_email_ids, relevance_scores)
        self.test_cases = [
            # 1. Exact Content Matches
            {
                "query": "Find emails about lunch plans",
                "relevant_ids": [3],
                "relevance_scores": {3: 3},
                "description": "Testing exact content match"
            },
            {
                "query": "Show me the meeting agenda",
                "relevant_ids": [1],
                "relevance_scores": {1: 3},
                "description": "Testing exact subject match"
            },
            
            # 2. Semantic Matches
            {
                "query": "What are the project status updates?",
                "relevant_ids": [2],
                "relevance_scores": {2: 3},
                "description": "Testing semantic understanding (updates vs status)"
            },
            {
                "query": "Find emails about food",
                "relevant_ids": [3],
                "relevance_scores": {3: 2},
                "description": "Testing semantic relationship (lunch vs food)"
            },
            
            # 3. Multiple Relevant Documents with Graded Relevance
            {
                "query": "Find all work-related discussions",
                "relevant_ids": [1, 2],
                "relevance_scores": {1: 3, 2: 3},
                "description": "Testing multiple equally relevant documents"
            },
            {
                "query": "Show me all scheduled events",
                "relevant_ids": [1, 3],
                "relevance_scores": {1: 3, 3: 2},  # Meeting more relevant than lunch
                "description": "Testing multiple documents with different relevance"
            },
            
            # 4. Sender/Recipient Based Queries
            {
                "query": "Find emails from emily",
                "relevant_ids": [3],
                "relevance_scores": {3: 3},
                "description": "Testing sender match"
            },
            {
                "query": "Show emails sent to bob.jones",
                "relevant_ids": [1],
                "relevance_scores": {1: 3},
                "description": "Testing recipient match"
            },
            
            # 5. Time-Based Queries
            {
                "query": "Find emails from October 11",
                "relevant_ids": [2, 3],
                "relevance_scores": {2: 2, 3: 2},
                "description": "Testing exact date match"
            },
            {
                "query": "Show me recent emails",
                "relevant_ids": [1, 2, 3],
                "relevance_scores": {3: 3, 2: 2, 1: 1},  # More recent = more relevant
                "description": "Testing temporal relevance"
            },
            
            # 6. Complex Multi-Aspect Queries
            {
                "query": "Find work meetings from john",
                "relevant_ids": [1],
                "relevance_scores": {1: 3},
                "description": "Testing combination of content and sender"
            },
            {
                "query": "Show recent project discussions with attachments",
                "relevant_ids": [1, 2],
                "relevance_scores": {2: 3, 1: 2},  # Project update more relevant
                "description": "Testing multiple aspects (time + content + attachment)"
            },
            
            # 7. Negative Tests
            {
                "query": "Find emails about vacation",
                "relevant_ids": [],
                "relevance_scores": {},
                "description": "Testing queries with no relevant results"
            },
            {
                "query": "Show emails from david",
                "relevant_ids": [],
                "relevance_scores": {},
                "description": "Testing non-existent sender"
            },
            
            # 8. Partial Information Queries
            {
                "query": "Find meeting",
                "relevant_ids": [1],
                "relevance_scores": {1: 3},
                "description": "Testing single keyword search"
            },
            {
                "query": "Show emails with attachments",
                "relevant_ids": [1],
                "relevance_scores": {1: 2},  # Mentioned attachments
                "description": "Testing attachment inference"
            },
            
            # 9. Context-Aware Queries
            {
                "query": "Find replies to admin",
                "relevant_ids": [1],
                "relevance_scores": {1: 2},
                "description": "Testing email thread context"
            },
            {
                "query": "Show forwarded messages",
                "relevant_ids": [1, 2],
                "relevance_scores": {1: 2, 2: 2},
                "description": "Testing email format understanding"
            },
            
            # 10. Intent-Based Queries
            {
                "query": "Find social plans",
                "relevant_ids": [3],
                "relevance_scores": {3: 3},
                "description": "Testing intent understanding (lunch = social)"
            },
            {
                "query": "Show task assignments",
                "relevant_ids": [2],
                "relevance_scores": {2: 2},
                "description": "Testing work context understanding"
            }
        ]
    
    def retrieve(self, query: str) -> List[int]:
        """Wrapper around the retrieval function"""
        return retrieve_emails(query, self.email_embeddings, top_k=10)
    
    def evaluate_query(self, query: str, relevant_ids: List[int], 
                      relevance_scores: Dict[int, float], k: int = 10) -> Dict[str, float]:
        """Evaluate a single query using multiple metrics"""
        
        # Get ranked results from retrieval function
        retrieved_ids = self.retrieve(query)
        
        # Convert to relevance list (0 if not relevant)
        relevances = [relevance_scores.get(id_, 0) for id_ in retrieved_ids]
        ideal_relevances = sorted([score for score in relevance_scores.values()], reverse=True)
        
        # Calculate metrics
        metrics = {
            f"ndcg@{k}": ndcg_at_k(relevances, ideal_relevances, k),
            f"precision@{k}": precision_at_k(relevances, k),
            f"recall@{k}": recall_at_k(relevances, len(relevant_ids), k)
        }
        
        return metrics
    
    def evaluate_all(self, k: int = 10) -> Dict[str, float]:
        """Evaluate all test cases and return average metrics"""
        all_metrics = []
        
        for test_case in self.test_cases:
            metrics = self.evaluate_query(
                test_case["query"],
                test_case["relevant_ids"],
                test_case["relevance_scores"],
                k
            )
            all_metrics.append(metrics)
        
        # Calculate averages
        avg_metrics = {}
        for metric in all_metrics[0].keys():
            avg_metrics[f"avg_{metric}"] = np.mean([m[metric] for m in all_metrics])
            
        return avg_metrics

def main():
    # Load emails
    with open('dataset1.json', 'r') as f:
        emails = json.load(f)
    
    # Initialize evaluator with actual retrieval implementation
    evaluator = EmailEvaluator(emails)
    
    # Evaluate each test case
    print("\nDetailed Evaluation Results:")
    print("-" * 50)
    
    all_metrics = []
    for i, test_case in enumerate(evaluator.test_cases, 1):
        metrics = evaluator.evaluate_query(
            test_case["query"],
            test_case["relevant_ids"],
            test_case["relevance_scores"],
            k=10
        )
        all_metrics.append(metrics)
        
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print(f"Relevant IDs: {test_case['relevant_ids']}")
        print("Metrics:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.3f}")
    
    # Calculate and display averages
    print("\nOverall Averages:")
    print("-" * 50)
    avg_metrics = {}
    for metric in all_metrics[0].keys():
        avg_metrics[f"avg_{metric}"] = np.mean([m[metric] for m in all_metrics])
        print(f"{metric}: {avg_metrics[f'avg_{metric}']:.3f}")

if __name__ == "__main__":
    main()
