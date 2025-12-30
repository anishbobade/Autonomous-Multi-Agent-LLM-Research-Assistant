import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl

# Handle SSL certificate for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK resources to /tmp which is writable
import os
nltk_data_dir = '/tmp/nltk_data'
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download all required NLTK data
required_packages = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'punkt_tab', 'omw-1.4']
for package in required_packages:
    try:
        nltk.download(package, quiet=True, download_dir=nltk_data_dir)
    except:
        pass

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def extract_text(paper):
    """Extract and combine all text from a paper."""
    text_parts = [
        paper.get('title', ''),
        paper.get('abstract', ''),
    ]
    return ' '.join(filter(None, text_parts))

def clean_text(text):
    """Clean text: lowercase, remove special chars, extra whitespace."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits, keep only letters and spaces
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_and_clean(text):
    """Tokenize, remove stop words, and lemmatize."""
    # Tokenize into words
    tokens = word_tokenize(text)
    
    # Remove stop words and apply lemmatization
    cleaned_tokens = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in stop_words and len(token) > 2  # Keep tokens > 2 chars
    ]
    
    return cleaned_tokens

# Process all papers through NLP pipeline
processed_papers = []

print("=" * 80)
print("NLP PIPELINE: TEXT EXTRACTION, TOKENIZATION & CLEANING")
print("=" * 80)

for idx, paper in enumerate(sample_papers, 1):
    print(f"\n{'='*80}")
    print(f"Processing Paper {idx}: {paper['title'][:60]}...")
    print('='*80)
    
    # Step 1: Extract text
    raw_text = extract_text(paper)
    print(f"\n✓ Step 1: Text Extraction")
    print(f"  - Raw text length: {len(raw_text)} characters")
    
    # Step 2: Clean text
    cleaned_text = clean_text(raw_text)
    print(f"\n✓ Step 2: Text Cleaning (lowercase, remove special chars)")
    print(f"  - Cleaned text length: {len(cleaned_text)} characters")
    print(f"  - Preview: {cleaned_text[:150]}...")
    
    # Step 3: Tokenize into sentences for chunking later
    sentences = sent_tokenize(raw_text)
    print(f"\n✓ Step 3: Sentence Tokenization")
    print(f"  - Total sentences: {len(sentences)}")
    
    # Step 4: Tokenize and clean (remove stop words, lemmatize)
    tokens = tokenize_and_clean(cleaned_text)
    print(f"\n✓ Step 4: Word Tokenization & Cleaning")
    print(f"  - Total tokens: {len(tokens)}")
    print(f"  - Sample tokens (first 20): {tokens[:20]}")
    
    # Store processed data
    processed_papers.append({
        'paper_id': idx,
        'title': paper['title'],
        'raw_text': raw_text,
        'cleaned_text': cleaned_text,
        'sentences': sentences,
        'tokens': tokens,
        'token_count': len(tokens),
        'sentence_count': len(sentences),
        'keywords': paper['keywords']
    })

print(f"\n\n{'='*80}")
print("PIPELINE SUMMARY")
print('='*80)
print(f"✅ Total papers processed: {len(processed_papers)}")
print(f"✅ Total tokens extracted: {sum(p['token_count'] for p in processed_papers):,}")
print(f"✅ Total sentences: {sum(p['sentence_count'] for p in processed_papers)}")
print(f"\nProcessed papers ready for chunk segmentation!")
print('='*80)
