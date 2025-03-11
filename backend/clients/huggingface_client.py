from transformers import pipeline

class HuggingFaceClient:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
    def generate_title(self, text: str, max_length: int = 10) -> str:
        summary = self.summarizer(text, max_length=max_length, min_length=3, do_sample=False)
        return summary[0]['summary_text'].strip()