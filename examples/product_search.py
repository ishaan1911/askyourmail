"""
Example: Using the Semantic Search Engine for product search
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval import SemanticRetriever

def main():
    # Sample product catalog
    products = [
        {
            "id": 1,
            "name": "Blue Cotton T-Shirt",
            "description": "Comfortable cotton t-shirt in navy blue color. Perfect for casual wear.",
            "price": 29.99,
            "category": "Clothing"
        },
        {
            "id": 2,
            "name": "Leather Wallet",
            "description": "Genuine leather wallet with multiple card slots and coin pocket.",
            "price": 49.99,
            "category": "Accessories"
        },
        {
            "id": 3,
            "name": "Wireless Headphones",
            "description": "Bluetooth headphones with noise cancellation and 20-hour battery life.",
            "price": 199.99,
            "category": "Electronics"
        }
    ]

    # Initialize retriever with description as the main content field
    retriever = SemanticRetriever(content_field="description")
    
    # Add products to the index
    print("Adding products to index...")
    retriever.add_items(products)
    
    # Example queries
    queries = [
        "comfortable clothing",
        "leather accessories",
        "audio devices with long battery",
        "blue casual wear",
        "wallet with card storage"
    ]
    
    # Search and display results
    print("\nSearching products...")
    for query in queries:
        print(f"\nQuery: {query}")
        results = retriever.search(query, k=2)
        
        for doc_id, score in results:
            product = products[doc_id]
            print(f"- {product['name']} (Score: {score:.3f})")
            print(f"  Price: ${product['price']}")
            print(f"  Category: {product['category']}")

if __name__ == "__main__":
    main()
