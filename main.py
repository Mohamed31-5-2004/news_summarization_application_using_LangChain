import os
import argparse
from news_retriever import search_articles
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager

# GUI support
from gui import NewsGUI
import tkinter as tk


# Default keys (use env variables or replace here)
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY") or "ad5c9285e3524426b13ddfa0a3ce94c3"


def demo_run(topic="artificial intelligence"):
    print(f"Running demo search for: {topic}\n")
    um = UserManager()
    emb = EmbeddingEngine()
    summ = Summarizer()

    articles = search_articles(topic, NEWSAPI_KEY, page_size=5)
    if not articles:
        print("No articles found.")
        return
    texts = [a.get("content") or a.get("description") or a.get("title") for a in articles]
    metadatas = [{"title": a.get("title"), "url": a.get("url"), "source": a.get("source")} for a in articles]
    ids = [a.get("id") for a in articles]

    emb.add_documents(texts=texts, metadatas=metadatas, ids=ids)
    # semantic search using the same topic
    results = emb.similarity_search(topic, k=3)

    for i, r in enumerate(results, 1):
        text = r.page_content
        meta = r.metadata or {}
        print(f"--- Result {i}: {meta.get('title')} ({meta.get('source')})\nURL: {meta.get('url')}\n")
        brief = summ.summarize(text, mode="brief")
        detailed = summ.summarize(text, mode="detailed")
        print("Brief summary:", brief)
        print("Detailed summary:", detailed)
        print("\n")

    um.add_history(topic, len(articles), "demo")
    print("Demo complete.")


def interactive():
    um = UserManager()
    emb = EmbeddingEngine()
    summ = Summarizer()

    while True:
        print("\nNews Summarizer - Options:\n1) Search topic  2) Save topic  3) View saved topics  4) View history  5) Demo topic  6) Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            topic = input("Enter topic to search: ")
            summary_type = input("Summary type ('brief' or 'detailed'): ") or "brief"
            articles = search_articles(topic, NEWSAPI_KEY, page_size=5)
            if not articles:
                print("No articles found.")
                continue
            texts = [a.get("content") or a.get("description") or a.get("title") for a in articles]
            metadatas = [{"title": a.get("title"), "url": a.get("url"), "source": a.get("source")} for a in articles]
            ids = [a.get("id") for a in articles]
            emb.add_documents(texts=texts, metadatas=metadatas, ids=ids)
            results = emb.similarity_search(topic, k=5)
            for i, r in enumerate(results, 1):
                text = r.page_content
                meta = r.metadata or {}
                print(f"\n--- Article {i}: {meta.get('title')} ({meta.get('source')})\nURL: {meta.get('url')}\n")
                print(summ.summarize(text, mode=summary_type))
            um.add_history(topic, len(articles), summary_type)
        elif choice == "2":
            topic = input("Topic to save: ")
            um.add_preference(topic)
            print("Saved.")
        elif choice == "3":
            prefs = um.get_preferences()
            print("Saved topics:")
            for p in prefs:
                print("-", p)
        elif choice == "4":
            hist = um.get_history()
            print("Search history:")
            for h in hist:
                print(h)
        elif choice == "5":
            topic = input("Demo topic: ")
            demo_run(topic)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run a short demo search and exit")
    parser.add_argument("--topic", type=str, help="Topic for demo run")
    parser.add_argument("--gui", action="store_true", help="Launch graphical interface")
    args = parser.parse_args()
    if args.gui:
        root = tk.Tk()
        NewsGUI(root)
        root.mainloop()
    elif args.demo:
        demo_run(args.topic or "artificial intelligence")
    else:
        interactive()
