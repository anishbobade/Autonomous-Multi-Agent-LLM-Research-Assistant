from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

print("=" * 80)
print("SEMANTIC EMBEDDING GENERATION")
print("=" * 80)

# Using TF-IDF for semantic embeddings (lightweight alternative to transformers)
print("\n🔧 Creating TF-IDF Vectorizer...")
print("   - Creates semantic vector representations")
print("   - Optimized for semantic similarity search")
print("   - Captures term importance and document relationships")

# Extract text chunks for embedding
chunk_texts = [chunk['chunk_text'] for chunk in all_text_chunks]

print(f"\n📊 Generating embeddings for {len(chunk_texts)} text chunks...")

# Create TF-IDF vectorizer with optimized parameters
tfidf_vectorizer = TfidfVectorizer(
    max_features=500,  # Limit dimensionality
    ngram_range=(1, 2),  # Unigrams and bigrams for better context
    min_df=1,
    max_df=0.95,
    sublinear_tf=True,  # Better term frequency scaling
    norm='l2'  # Normalize for cosine similarity
)

# Generate embeddings
chunk_embeddings = tfidf_vectorizer.fit_transform(chunk_texts).toarray()

print(f"\n✅ Generated embeddings!")
print(f"   Shape: {chunk_embeddings.shape}")
print(f"   Dimensions: {chunk_embeddings.shape[1]}")
print(f"   Data type: {chunk_embeddings.dtype}")
print(f"   Vocabulary size: {len(tfidf_vectorizer.vocabulary_)}")

# Create enhanced knowledge base with embeddings
knowledge_base = []
for idx, chunk in enumerate(all_text_chunks):
    knowledge_base.append({
        'chunk_id': chunk['chunk_id'],
        'paper_id': chunk['paper_id'],
        'paper_title': chunk['paper_title'],
        'position': chunk['position'],
        'chunk_text': chunk['chunk_text'],
        'token_count': chunk['token_count'],
        'embedding': chunk_embeddings[idx],
        'embedding_norm': float(np.linalg.norm(chunk_embeddings[idx]))
    })

print("\n" + "=" * 80)
print("KNOWLEDGE BASE STATISTICS")
print("=" * 80)
print(f"Total entries: {len(knowledge_base)}")
print(f"Unique papers: {len(set(k['paper_id'] for k in knowledge_base))}")
print(f"Average tokens per chunk: {np.mean([k['token_count'] for k in knowledge_base]):.1f}")
print(f"Embedding dimension: {knowledge_base[0]['embedding'].shape[0]}")
print(f"Average embedding norm: {np.mean([k['embedding_norm'] for k in knowledge_base]):.3f}")
print(f"Sparsity: {100 * (1 - np.count_nonzero(chunk_embeddings) / chunk_embeddings.size):.1f}%")

# Display sample entries
print("\n" + "=" * 80)
print("SAMPLE KNOWLEDGE BASE ENTRIES")
print("=" * 80)

for i in range(min(3, len(knowledge_base))):
    entry = knowledge_base[i]
    print(f"\n📑 Entry {i+1}: {entry['chunk_id']}")
    print(f"   Paper: {entry['paper_title'][:60]}...")
    print(f"   Tokens: {entry['token_count']}")
    print(f"   Non-zero features: {np.count_nonzero(entry['embedding'])}")
    print(f"   Top features: {entry['embedding'][:5].round(4).tolist()}...")
    print(f"   Text preview: {entry['chunk_text'][:100]}...")

print("\n" + "=" * 80)
print("✅ Embedded knowledge base ready for semantic search!")
print("=" * 80)
