import nltk

def download_nltk_resources():
    """Downloads required NLTK datasets and models"""
    resources = [
        ('punkt', 'Tokenizer models'),
        ('stopwords', 'Stop words list'),
        ('wordnet', 'Lexical database'),
        ('omw-1.4', 'Multilingual wordnet')
    ]
    
    for resource, desc in resources:
        try:
            print(f"Downloading {resource} ({desc})...")
            nltk.download(resource, quiet=False)
            print(f"✓ {resource} installed successfully\n")
        except Exception as e:
            print(f"✗ Error downloading {resource}: {str(e)}\n")

if __name__ == "__main__":
    print("Starting NLTK setup...\n")

    download_nltk_resources()
    
    print("\nSetup completed. Verify installation with:")
    print("python -c \"import nltk; print(nltk.data.find('tokenizers/punkt'))\"") 