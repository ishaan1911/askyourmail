# Semantic Search Engine

A powerful and scalable semantic search engine that can handle any type of data using OpenAI's embeddings and FAISS for efficient similarity search.

## Features

- 🔍 **Universal Data Support**: Works with any type of text data (emails, documents, products, etc.)
- 🚀 **Highly Scalable**: Efficiently handles millions of documents using FAISS indexing
- 💪 **Performance Optimized**: 
  - Batch processing
  - Parallel query processing
  - Memory-efficient operations
- 🔧 **Flexible Configuration**:
  - Multiple similarity metrics (L2, cosine)
  - Configurable batch sizes
  - Adjustable similarity thresholds
- 🔒 **Production Ready**:
  - Thread-safe operations
  - Error handling
  - Comprehensive logging

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd email_retrieval
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
Create a `key.env` file in the project root:
```env
OPENAI_API_KEY=your_api_key_here
```

## Quick Start

```python
from retrieval import SemanticRetriever

# Initialize the retriever
retriever = SemanticRetriever()

# Add items to the index
documents = [
    {"content": "First document content"},
    {"content": "Second document content"},
    {"content": "Third document content"}
]
retriever.add_items(documents)

# Search
results = retriever.search("your search query", k=3)
for doc_id, score in results:
    print(f"Document {doc_id}: Score {score}")
```

## Advanced Usage

### Custom Data Types
```python
# Configure content field for your data structure
retriever = SemanticRetriever(content_field="description")

# Add custom items
products = [
    {"id": 1, "description": "Blue cotton shirt", "price": 29.99},
    {"id": 2, "description": "Black leather shoes", "price": 89.99}
]
retriever.add_items(products)
```

### Batch Processing
```python
# Process multiple queries in parallel
queries = ["query1", "query2", "query3"]
results = retriever.batch_search(queries, k=5, max_workers=4)
```

### Update Items
```python
# Update existing items
success = retriever.update_item(
    item_id=1,
    new_item={"content": "Updated content"}
)
```

## Evaluation

Run the evaluation suite:
```bash
python evaluation.py
```

This will test the system against various scenarios:
- Exact matches
- Semantic understanding
- Multiple relevant documents
- Graded relevance
- Time-based queries
- And more...

## Project Structure

- `main.py`: Entry point and example usage
- `embeddings.py`: Embedding generation logic
- `retrieval.py`: Core search functionality
- `evaluation.py`: Test suite and metrics
- `requirements.txt`: Project dependencies
- `key.env`: Configuration file (not included in repo)

## Performance Considerations

- For large datasets (>1M items), consider using GPU acceleration with `faiss-gpu`
- Adjust batch_size based on your memory constraints
- Use threshold parameter to filter low-quality matches
- Consider using parallel processing for large batch operations

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
