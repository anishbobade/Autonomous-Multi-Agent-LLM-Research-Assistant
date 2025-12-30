from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

print("=" * 80)
print("SEMANTIC SEARCH SYSTEM")
print("=" * 80)

def semantic_search(query, top_k=3):
    """
    Perform semantic similarity search on the knowledge base.
    
    Args:
        query: Search query string
        top_k: Number of top results to return
    
    Returns:
        List of top matching chunks with similarity scores
    """
    # Transform query using the same vectorizer
    query_embedding = tfidf_vectorizer.transform([query]).toarray()
    
    # Calculate cosine similarity with all chunks
    embeddings_matrix = np.array([k['embedding'] for k in knowledge_base])
    similarities = cosine_similarity(query_embedding, embeddings_matrix)[0]
    
    # Get top-k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'rank': len(results) + 1,
            'similarity': float(similarities[idx]),
            'chunk_id': knowledge_base[idx]['chunk_id'],
            'paper_id': knowledge_base[idx]['paper_id'],
            'paper_title': knowledge_base[idx]['paper_title'],
            'chunk_text': knowledge_base[idx]['chunk_text'],
            'token_count': knowledge_base[idx]['token_count']
        })
    
    return results

# Test the semantic search system with sample queries
test_queries = [
    "deep learning diagnostic accuracy",
    "clinical decision support artificial intelligence",
    "natural language processing medical records"
]

print("\n🔍 SEMANTIC SEARCH DEMONSTRATIONS")
print("=" * 80)

for query_idx, query in enumerate(test_queries):
    print(f"\n\n{'='*80}")
    print(f"QUERY {query_idx + 1}: '{query}'")
    print('='*80)
    
    search_results = semantic_search(query, top_k=2)
    
    for result in search_results:
        print(f"\n🎯 Rank {result['rank']} | Similarity: {result['similarity']:.4f}")
        print(f"   Chunk ID: {result['chunk_id']}")
        print(f"   Paper: {result['paper_title'][:70]}...")
        print(f"   Tokens: {result['token_count']}")
        print(f"   Text: {result['chunk_text'][:150]}...")

print("\n\n" + "=" * 80)
print("SEMANTIC SEARCH SYSTEM SUMMARY")
print("=" * 80)
print(f"✅ Knowledge base entries: {len(knowledge_base)}")
print(f"✅ Embedding dimensions: {knowledge_base[0]['embedding'].shape[0]}")
print(f"✅ Search method: Cosine similarity")
print(f"✅ Vectorization: TF-IDF with bigrams")
print(f"✅ Tested queries: {len(test_queries)}")
print("\n🎉 Semantic search system ready for use!")
print("=" * 80)

# Create search function for external use
print("\n💡 Usage Example:")
print("   results = semantic_search('your query here', top_k=5)")
print("   for r in results:")
print("       print(f\"{r['rank']}. {r['paper_title']} (score: {r['similarity']:.3f})\")")
