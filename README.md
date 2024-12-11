# Email Dataset Analyzer

This is a simple tool to analyze email datasets and perform queries on them.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Place your email dataset (CSV format) in the project directory.

## Usage

1. Import the EmailAnalyzer class:
```python
from email_analyzer import EmailAnalyzer
```

2. Create an instance with your dataset:
```python
analyzer = EmailAnalyzer('email_thread_details.csv')
```

3. Search through the dataset:
```python
results = analyzer.search('your query here')
print(results)
```

4. Get dataset statistics:
```python
stats = analyzer.get_statistics()
print(stats)
```

## Features

- Search across all columns in the dataset
- Basic statistics about the dataset
- Support for CSV format email datasets

## Additional Information

- This project now includes evaluation pairs and tests for the email analyzer functionality.

# AskYourMail 

A powerful semantic email search system that understands natural language queries. Find exactly what you're looking for in your emails using plain English questions.

## Features

- **Natural Language Search**: Ask questions in plain English
  - "Find emails about lunch plans"
  - "Find project updates from last October"

- **Smart Search Capabilities**:
  - Semantic understanding (finds related content)
  - Search by sender/recipient
  - Date-based search
  - Content and subject search
  - Combined search criteria

- **User-Friendly Interface**:
  - Colored output for better readability
  - Search term highlighting
  - Interactive email viewing
  - Relevance scoring

## Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ishaan1911/askyourmail.git
   cd askyourmail
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Example Queries

- "Find emails about lunch plans"
- "Show me emails from john.doe about meetings"
- "Show project updates"
- "Find emails with attachments about the budget"

## Technical Details

- Uses OpenAI's embeddings for semantic understanding
- FAISS for efficient similarity search
- Supports various email formats

## Project Structure

```
askyourmail/
├── email_analyzer.py
├── requirements.txt
├── README.md
└── test_email_analyzer.py
```

## Advanced Usage

See [GUIDE.md](GUIDE.md) for:
- Detailed feature documentation
- Performance optimization
- Troubleshooting

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for embeddings API
- FAISS team for similarity search

## Contact

For questions or support:
- Create an issue on GitHub

---
Made with ❤️ by Ishaan Parekh
