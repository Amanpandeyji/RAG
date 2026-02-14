#  DSA Learning Assistant with RAG

A beginner-friendly Data Structures and Algorithms (DSA) assistant built using Retrieval-Augmented Generation (RAG) with Groq API.

##  Features

- **RAG-Powered**: Uses retrieval-augmented generation to answer questions based only on provided DSA notes
- **Beginner-Friendly**: Explains concepts in simple, easy-to-understand language
- **Context-Aware**: Only uses information from the notes - no hallucinations!
- **Fast Responses**: Powered by Groq's ultra-fast LLM inference
- **Interactive Mode**: Chat-based interface for learning

##  Architecture

```
User Question → Embedding → Vector Search → Retrieve Context → Groq LLM → Answer
```

1. **Document Loading**: Loads DSA notes from text file
2. **Chunking**: Splits notes into manageable chunks
3. **Embedding**: Converts chunks to vector embeddings
4. **Vector Store**: Stores embeddings in ChromaDB
5. **Retrieval**: Finds most relevant chunks for user question
6. **Generation**: Groq LLM generates answer using retrieved context

##  Prerequisites

- Python 3.8 or higher
- Groq API key

##  Quick Start

### Local Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/dsa-learning-assistant.git
cd dsa-learning-assistant
```

2. **Create virtual environment** (optional but recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your actual Groq API key
GROQ_API_KEY=your_actual_api_key_here
```

5. **Run the Streamlit app**:
```bash
streamlit run app.py
```

Or use the command-line interface:
```bash
python dsa_assistant.py
```

## Usage

### Interactive Mode (Recommended)

Run the assistant in chat mode:

```bash
python dsa_assistant.py
```

Then ask questions like:
- "What is an array?"
- "How does binary search work?"
- "Explain recursion in simple terms"
- "What is the time complexity of bubble sort?"

Type `exit` or `quit` to end the session.

### Example Questions

Run pre-defined example questions:

```bash
python example_usage.py
```

### Programmatic Usage

```python
from dsa_assistant import DSAAssistant

# Initialize
assistant = DSAAssistant()

# Ask a question
answer = assistant.ask("What is a linked list?")
print(answer)
```

## DSA Notes

The assistant uses `dsa_notes.txt` which contains beginner-friendly explanations of:

- **Arrays**: Operations, time complexity, common problems
- **Linked Lists**: Types, operations, cycle detection
- **Stacks & Queues**: LIFO vs FIFO, applications
- **Sorting**: Bubble, Selection, Insertion, Merge, Quick Sort
- **Searching**: Linear and Binary Search
- **Big O Notation**: Time complexity explained simply
- **Recursion**: Base cases, recursive cases, examples
- **Trees**: Binary trees, BST, traversals

##  Customization

### Add More Notes

Edit `dsa_notes.txt` to add more topics:
```bash
# Just append to the file
echo "\n## Hash Tables\n..." >> dsa_notes.txt
```

Then re-run to rebuild the vector store.

### Change LLM Model

In `dsa_assistant.py`, modify the model:
```python
self.llm = ChatGroq(
    groq_api_key=self.groq_api_key,
    model_name="llama3-70b-8192",  # or other Groq models
    temperature=0
)
```

Available Groq models:
- `mixtral-8x7b-32768` (default - good balance)
- `llama3-70b-8192` (more powerful)
- `llama3-8b-8192` (faster, lighter)
- `gemma-7b-it` (efficient)

### Adjust Retrieval

Change the number of context chunks retrieved:
```python
retriever=self.vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Retrieve top 5 chunks instead of 3
)
```

##  How It Works

### 1. Document Processing
```
dsa_notes.txt → Text Splitter → Chunks (1000 chars each, 200 overlap)
```

### 2. Embedding & Storage
```
Chunks → HuggingFace Embeddings → ChromaDB Vector Store
```

### 3. Query Processing
```
User Query → Embedding → Similarity Search → Top 3 Relevant Chunks
```

### 4. Answer Generation
```
Retrieved Context + User Query + Prompt Template → Groq LLM → Answer
```

##  Rules Enforced

The assistant follows strict rules:

1.  Uses ONLY the provided context
2.  Explains in simple, beginner-friendly language
3.  Says "not available" if answer isn't in notes
4.  No assumptions about advanced knowledge
5.  No invented algorithms or shortcuts
6.  Follows examples from the context

##  Example Output

```
 Question: What is binary search?

 Searching through DSA notes...

 Answer:
Binary search is a searching algorithm that only works on SORTED arrays. 
Think of it like finding a word in a dictionary - you open it in the middle 
and decide which half to search.

Here's how it works:
1. Find the middle element
2. If your target is smaller, search the left half
3. If your target is larger, search the right half
4. Repeat until found or no elements left

Time Complexity: O(log n) - Very fast!
Space Complexity: O(1) for iterative, O(log n) for recursive

Use binary search when: Your array is sorted

📖 Retrieved 3 relevant sections from notes
```

##  Troubleshooting

### "GROQ_API_KEY not found"
- Check that `.env` file exists in the same directory
- Verify the API key is correct

### "Notes file not found"
- Ensure `dsa_notes.txt` exists in the same directory
- Check file permissions

### Slow first run
- First run downloads the embedding model (~80MB)
- Subsequent runs are much faster

### Import errors
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## File Structure
```
RAG/
├── dsa_assistant.py      # Main assistant class
├── example_usage.py      # Example questions
├── dsa_notes.txt         # DSA knowledge base
├── requirements.txt      # Python dependencies
├── .env                  # API key (keep secret!)
├── README.md            # This file
└── chroma_db/           # Vector store (auto-created)
```

## 🎓 Learning Tips

1. **Start with basics**: Ask about simple topics first (arrays, loops)
2. **Build gradually**: Move to complex topics (recursion, trees)
3. **Ask for examples**: Request examples from the notes
4. **Compare concepts**: Ask about differences (stack vs queue)
5. **Understand complexity**: Learn about Big O notation

## � Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Add `GROQ_API_KEY` to secrets
5. Deploy!

** Complete deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
-  Streamlit Cloud (recommended)
-  Docker deployment
- Railway, Render, Heroku options
- Security best practices
- Troubleshooting tips

### Docker Deployment

```bash
# Build
docker build -t dsa-assistant .

# Run
docker run -p 8501:8501 -e GROQ_API_KEY=your_key dsa-assistant

# Or use docker-compose
docker-compose up -d
```

##  Security Note

 **IMPORTANT**: Never commit your API keys!

-  Keep `.env` file private
-  Never hardcode API keys in code
-  Use `.env.example` as template
-  Add `.env` to `.gitignore`
-  Use environment variables in deployment

## 📄 License

This project is for educational purposes.

## Contributing

To add more DSA topics:
1. Edit `dsa_notes.txt`
2. Follow the same simple explanation style
3. Include examples and time complexities
4. Use beginner-friendly language

