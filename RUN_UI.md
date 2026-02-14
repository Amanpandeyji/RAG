# 🚀 Running the DSA Assistant Web UI

## Quick Start

1. **Install/Update dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit app:**
```bash
streamlit run app.py
```

3. **Open your browser:**
The app will automatically open at `http://localhost:8501`

## Features

### 🎨 Beautiful Interface
- Clean, modern design
- Easy-to-use chat interface
- Responsive layout

### 💡 Quick Topic Buttons
Click any topic in the sidebar:
- Arrays
- Linked Lists
- Stacks & Queues
- Binary Search
- Big O Notation
- Recursion
- Trees
- Sorting Algorithms

### 💬 Interactive Chat
- Type any DSA question
- Get instant, beginner-friendly answers
- View chat history
- Clear chat anytime

### 🎯 Smart Features
- **Context-Aware**: Only uses information from DSA notes
- **No Hallucinations**: Admits when info isn't available
- **Beginner-Friendly**: Simple explanations
- **Fast**: Powered by Groq's ultra-fast LLM

## Usage Tips

1. **Start Simple**: Click a topic button to see how it works
2. **Ask Naturally**: Type questions in plain English
3. **Be Specific**: "How does bubble sort work?" is better than just "sorting"
4. **Follow Up**: Ask related questions to dive deeper

## Troubleshooting

### Port Already in Use
If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Dependencies Issue
Make sure all packages are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Slow First Load
First run downloads the embedding model (~80MB). Subsequent runs are faster.

## Command Line Options

### Run on different port:
```bash
streamlit run app.py --server.port 8080
```

### Run on network (accessible from other devices):
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Auto-reload on code changes:
```bash
streamlit run app.py --server.fileWatcherType auto
```

## Enjoy Learning! 🎓

Your DSA learning journey starts now. Ask away and have fun! 🚀
