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
analyzer = EmailAnalyzer('your_email_dataset.csv')
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
