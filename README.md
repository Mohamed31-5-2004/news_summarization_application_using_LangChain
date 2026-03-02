News Summarizer (LangChain + Chroma + HuggingFace)

Setup

1. Create and activate a Python environment (Python 3.8+)

2. Install dependencies:

```
python -m pip install -r requirements.txt
```

3. Optional: set `NEWSAPI_KEY` environment variable. The script uses the sample key if unset.

Usage

- Run graphical interface (GUI):

```
python main.py --gui
```

- Run interactive CLI:

```
python main.py
```

- Run demo once and exit:

```
python main.py --demo --topic "artificial intelligence"
```

Files

- `news_retriever.py`: calls NewsAPI everything endpoint
- `embedding_engine.py`: embeddings via sentence-transformers and Chroma vector store
- `summarizer.py`: extractive (LexRank fallback) and abstractive (HuggingFace transformers) summarizers
- `user_manager.py`: stores user preferences and search history in JSON
- `main.py`: CLI, demo, and GUI launcher
- `gui.py`: Tkinter-based graphical interface with search, save topics, and history

Notes

- Models will be downloaded on first run. Ensure internet access.
- If transformer model downloads are too large, adjust `summarizer.py` to use a lighter model.

