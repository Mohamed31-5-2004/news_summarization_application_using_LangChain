import tkinter as tk
from tkinter import scrolledtext, messagebox

from news_retriever import search_articles
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager
import os

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY") or "ad5c9285e3524426b13ddfa0a3ce94c3"


class NewsGUI:
    def __init__(self, master):
        self.master = master
        master.title("News Summarizer")
        self.um = UserManager()
        self.emb = EmbeddingEngine()
        self.summ = Summarizer()

        tk.Label(master, text="Topic:").grid(row=0, column=0, sticky="w")
        self.topic_var = tk.StringVar()
        tk.Entry(master, textvariable=self.topic_var, width=40).grid(row=0, column=1, columnspan=2)

        tk.Label(master, text="Summary:").grid(row=1, column=0, sticky="w")
        self.summary_type = tk.StringVar(value="brief")
        tk.Radiobutton(master, text="Brief", variable=self.summary_type, value="brief").grid(row=1, column=1)
        tk.Radiobutton(master, text="Detailed", variable=self.summary_type, value="detailed").grid(row=1, column=2)

        tk.Button(master, text="Search", command=self.search).grid(row=2, column=0)
        tk.Button(master, text="Save Topic", command=self.save_topic).grid(row=2, column=1)
        tk.Button(master, text="View Preferences", command=self.view_prefs).grid(row=2, column=2)
        tk.Button(master, text="History", command=self.view_history).grid(row=2, column=3)

        self.output = scrolledtext.ScrolledText(master, width=80, height=20)
        self.output.grid(row=3, column=0, columnspan=4, pady=10)

    def search(self):
        topic = self.topic_var.get().strip()
        if not topic:
            messagebox.showwarning("Input needed", "Please enter a topic.")
            return
        articles = search_articles(topic, NEWSAPI_KEY, page_size=5)
        if not articles:
            messagebox.showinfo("No Results", "No articles found.")
            return
        texts = [a.get("content") or a.get("description") or a.get("title") for a in articles]
        metas = [{"title": a.get("title"), "url": a.get("url"), "source": a.get("source")} for a in articles]
        ids = [a.get("id") for a in articles]
        self.emb.add_documents(texts=texts, metadatas=metas, ids=ids)
        results = self.emb.similarity_search(topic, k=5)
        self.output.delete("1.0", tk.END)
        for i, r in enumerate(results, 1):
            text = r.page_content
            meta = r.metadata or {}
            self.output.insert(tk.END, f"--- Article {i}: {meta.get('title')} ({meta.get('source')})\nURL: {meta.get('url')}\n")
            summary = self.summ.summarize(text, mode=self.summary_type.get())
            self.output.insert(tk.END, summary + "\n\n")
        self.um.add_history(topic, len(articles), self.summary_type.get())

    def save_topic(self):
        topic = self.topic_var.get().strip()
        if not topic:
            messagebox.showwarning("Input needed", "Please enter a topic to save.")
            return
        self.um.add_preference(topic)
        messagebox.showinfo("Saved", f"Topic '{topic}' saved to preferences.")

    def view_prefs(self):
        prefs = self.um.get_preferences()
        messagebox.showinfo("Preferences", "\n".join(prefs) if prefs else "No saved topics.")

    def view_history(self):
        hist = self.um.get_history()
        text = "\n".join([str(h) for h in hist])
        messagebox.showinfo("History", text if text else "No history yet.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = NewsGUI(root)
    root.mainloop()
