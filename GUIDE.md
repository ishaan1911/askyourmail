# AskYourMail: Comprehensive Guide

## Overview
AskYourMail is an advanced semantic search engine that uses OpenAI's embeddings and FAISS to provide intelligent search capabilities across any type of data. Whether you're working with emails, documents, products, or any text-based data, this system can help you find relevant information using natural language queries.

## Key Features
- 🔍 **Universal Search**: Works with any text data type
- 🧠 **Semantic Understanding**: Understands meaning, not just keywords
- ⚡ **High Performance**: Handles millions of documents efficiently
- 🎯 **Accurate Results**: Uses state-of-the-art embedding models
- 🔄 **Real-time Updates**: Supports adding and updating documents

## Getting Started

### Prerequisites
1. Python 3.8 or higher
2. OpenAI API key
3. Git (for cloning the repository)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone git@github.com:ishaan1911/askyourmail.git
   cd askyourmail
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   Create a file named `key.env` in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Project Structure

```
askyourmail/
├── embeddings.py      # Handles text-to-vector conversion
├── retrieval.py       # Core search functionality
├── evaluation.py      # Testing and metrics
├── examples/          # Example implementations
│   ├── product_search.py
│   └── document_search.py
└── requirements.txt   # Project dependencies
```

## How It Works

1. **Text to Vectors**: 
   - The system converts text into high-dimensional vectors using OpenAI's embeddings
   - These vectors capture the semantic meaning of the text

2. **Efficient Storage**:
   - FAISS indexes these vectors for fast similarity search
   - Supports millions of documents with quick retrieval

3. **Smart Search**:
   - Converts search queries into the same vector space
   - Finds documents with similar meaning, not just matching words
   - Ranks results by relevance

## Usage Examples

### 1. Basic Search
```python
from retrieval import SemanticRetriever

# Initialize
retriever = SemanticRetriever()

# Add documents
documents = [
    {"content": "First document content"},
    {"content": "Second document content"}
]
retriever.add_items(documents)

# Search
results = retriever.search("your query here", k=3)
```

### 2. Product Search
```python
# Configure for product data
retriever = SemanticRetriever(content_field="description")

# Add products
products = [
    {
        "id": 1,
        "name": "Blue T-Shirt",
        "description": "Comfortable cotton shirt",
        "price": 29.99
    }
]
retriever.add_items(products)
```

### 3. Document Search
```python
# Search through documents
documents = [
    {
        "title": "AI Basics",
        "content": "Introduction to artificial intelligence...",
        "author": "John Doe"
    }
]
retriever.add_items(documents)
```

## Advanced Features

### 1. Batch Processing
```python
# Process multiple queries in parallel
queries = ["query1", "query2", "query3"]
results = retriever.batch_search(queries, k=5, max_workers=4)
```

### 2. Similarity Thresholds
```python
# Only return highly relevant results
results = retriever.search("query", k=5, threshold=0.8)
```

### 3. Custom Content Fields
```python
# Specify which field contains the text to search
retriever = SemanticRetriever(content_field="description")
```

## Performance Tips

1. **Batch Processing**
   - Use batch_embed() for multiple documents
   - Use batch_search() for multiple queries

2. **Memory Optimization**
   - Adjust batch_size based on your RAM
   - Use threshold to filter low-quality matches

3. **Speed Optimization**
   - Use FAISS GPU index for larger datasets
   - Enable parallel processing for batch operations

## Common Use Cases

1. **Email Search**
   - Search through email content and metadata
   - Find relevant conversations by topic
   - Group similar emails together

2. **Document Management**
   - Search through large document collections
   - Find related documents
   - Organize documents by topic

3. **Product Catalogs**
   - Natural language product search
   - Find similar products
   - Category organization

## Evaluation

The system includes a comprehensive evaluation framework:
```bash
python evaluation.py
```

This tests:
- Exact matches
- Semantic understanding
- Multiple relevant documents
- Graded relevance
- Time-based queries

## Troubleshooting

1. **Installation Issues**
   - Make sure you have Python 3.8+
   - Install system dependencies for FAISS
   - Check virtual environment activation

2. **Search Quality**
   - Verify API key is correct
   - Check document content quality
   - Adjust similarity thresholds

3. **Performance Issues**
   - Reduce batch sizes
   - Enable GPU acceleration
   - Use parallel processing

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Look through existing GitHub issues
3. Create a new issue with:
   - Problem description
   - Steps to reproduce
   - Error messages
   - System information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
