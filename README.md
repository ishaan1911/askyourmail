# AskYourMail 📧

A powerful semantic email search system that understands natural language queries. Find exactly what you're looking for in your emails using plain English questions.

## 🌟 Features

- **Natural Language Search**: Ask questions in plain English
  - "Find emails about lunch plans"
  - "Show me emails from John about meetings"
  - "Find project updates from last October"

- **Smart Search Capabilities**:
  - 🔍 Semantic understanding (finds related content)
  - 👤 Search by sender/recipient
  - 📅 Date-based search
  - 📝 Content and subject search
  - 🔄 Combined search criteria

- **User-Friendly Interface**:
  - 🎨 Colored output for better readability
  - ✨ Search term highlighting
  - 🖱️ Interactive email viewing
  - 📊 Relevance scoring

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ishaan1911/askyourmail.git
   cd askyourmail
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   Create a file named `key.env`:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the System**
   ```bash
   python main.py
   ```

## 💡 Example Queries

- "Find emails about lunch plans"
- "Show me emails from john.doe about meetings"
- "Find emails sent to bob.jones in October"
- "Show project updates"
- "Find emails with attachments about the budget"

## 🛠️ Technical Details

- Uses OpenAI's embeddings for semantic understanding
- FAISS for efficient similarity search
- Python-based implementation
- Supports various email formats

## 📚 Project Structure

```
askyourmail/
├── main.py           # Main search interface
├── embeddings.py     # Embedding generation
├── retrieval.py      # Search functionality
├── evaluation.py     # Testing & metrics
└── examples/         # Example implementations
```

## 🔧 Advanced Usage

See [GUIDE.md](GUIDE.md) for:
- Detailed feature documentation
- Advanced search techniques
- Performance optimization
- Troubleshooting

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for embeddings API
- FAISS team for similarity search
- All contributors and users

## 📬 Contact

For questions or support:
- Create an issue on GitHub
- Contact the maintainers

---
Made with ❤️ by Ishaan Parekh
