from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from transformers import pipeline


class Summarizer:
    def __init__(self):
        # Abstractive summarizer (smaller distil model)
        try:
            self.abstractive = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        except Exception:
            self.abstractive = None

    def brief_extractive(self, text, sentences_count=2):
        """Extractive summarization using LexRank (returns sentences_count sentences)."""
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LexRankSummarizer()
            summary_sentences = summarizer(parser.document, sentences_count)
            return " ".join([str(s) for s in summary_sentences])
        except Exception:
            # fallback simple heuristic: take first N sentences by splitting on punctuation
            import re

            sents = [s.strip() for s in re.split(r"(?<=[.!?]) +", text) if s.strip()]
            return " ".join(sents[:sentences_count])

    def detailed_abstractive(self, text, max_length=150):
        """Abstractive summarization via HuggingFace transformers pipeline."""
        if not self.abstractive:
            return "[abstractive model unavailable]"
        # transformers pipeline handles long text by truncation; keep it reasonable
        try:
            out = self.abstractive(text, max_length=max_length, min_length=60, do_sample=False)
            return out[0]["summary_text"]
        except Exception:
            return "[abstractive summarization failed]"

    def summarize(self, text, mode="brief"):
        if mode == "brief":
            return self.brief_extractive(text, sentences_count=2)
        else:
            return self.detailed_abstractive(text)
