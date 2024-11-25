"""
Example: Using the Semantic Search Engine for document search
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval import SemanticRetriever

def main():
    # Sample documents
    documents = [
        {
            "id": 1,
            "title": "Machine Learning Basics",
            "content": """
            Machine learning is a subset of artificial intelligence that focuses on developing
            systems that can learn from and make decisions based on data. It includes
            supervised learning, unsupervised learning, and reinforcement learning approaches.
            """,
            "author": "John Smith",
            "date": "2024-01-15"
        },
        {
            "id": 2,
            "title": "Data Preprocessing Guide",
            "content": """
            Data preprocessing is a crucial step in any data science project. It involves
            cleaning data, handling missing values, encoding categorical variables, and
            scaling numerical features to prepare them for machine learning models.
            """,
            "author": "Emily Johnson",
            "date": "2024-01-16"
        },
        {
            "id": 3,
            "title": "Neural Networks Explained",
            "content": """
            Neural networks are computing systems inspired by biological neural networks.
            They consist of layers of interconnected nodes that process and transform input
            data to generate meaningful predictions or classifications.
            """,
            "author": "Michael Brown",
            "date": "2024-01-17"
        }
    ]

    # Initialize retriever
    retriever = SemanticRetriever(content_field="content")
    
    # Add documents to the index
    print("Adding documents to index...")
    retriever.add_items(documents)
    
    # Example queries
    queries = [
        "what is machine learning",
        "how to prepare data for ML",
        "explain neural networks architecture",
        "supervised learning methods",
        "data cleaning techniques"
    ]
    
    # Search and display results
    print("\nSearching documents...")
    for query in queries:
        print(f"\nQuery: {query}")
        results = retriever.search(query, k=2)
        
        for doc_id, score in results:
            doc = documents[doc_id]
            print(f"- {doc['title']} (Score: {score:.3f})")
            print(f"  Author: {doc['author']}")
            print(f"  Date: {doc['date']}")
            print(f"  Preview: {doc['content'][:100]}...")

if __name__ == "__main__":
    main()
