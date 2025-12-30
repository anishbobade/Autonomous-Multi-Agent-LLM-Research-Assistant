import pandas as pd

def create_chunks(paper_data, chunk_size=100, overlap=20):
    """
    Segment text into overlapping chunks based on token count.
    
    Args:
        paper_data: Processed paper dictionary
        chunk_size: Target number of tokens per chunk
        overlap: Number of tokens to overlap between chunks
    
    Returns:
        List of chunk dictionaries
    """
    tokens = paper_data['tokens']
    sentences = paper_data['sentences']
    
    chunks = []
    chunk_id = 1
    
    # Create token-based chunks with overlap
    start_idx = 0
    while start_idx < len(tokens):
        end_idx = min(start_idx + chunk_size, len(tokens))
        chunk_tokens = tokens[start_idx:end_idx]
        
        # Reconstruct text from tokens (approximation)
        chunk_text = ' '.join(chunk_tokens)
        
        chunks.append({
            'chunk_id': f"{paper_data['paper_id']}-{chunk_id}",
            'paper_id': paper_data['paper_id'],
            'paper_title': paper_data['title'],
            'chunk_tokens': chunk_tokens,
            'token_count': len(chunk_tokens),
            'chunk_text': chunk_text,
            'position': chunk_id
        })
        
        chunk_id += 1
        start_idx += (chunk_size - overlap)
        
        # Stop if we're at the end
        if end_idx >= len(tokens):
            break
    
    return chunks

# Segment all processed papers into chunks
all_text_chunks = []

print("=" * 80)
print("TEXT CHUNK SEGMENTATION")
print("=" * 80)
print("\nSegmentation Parameters:")
print("  - Chunk size: 100 tokens")
print("  - Overlap: 20 tokens")
print("=" * 80)

for paper_data in processed_papers:
    paper_chunks = create_chunks(paper_data, chunk_size=100, overlap=20)
    all_text_chunks.extend(paper_chunks)
    
    print(f"\n📄 Paper {paper_data['paper_id']}: {paper_data['title'][:60]}...")
    print(f"   Total tokens: {paper_data['token_count']}")
    print(f"   Generated chunks: {len(paper_chunks)}")
    
    for chunk in paper_chunks:
        print(f"\n   Chunk {chunk['chunk_id']}:")
        print(f"     - Tokens: {chunk['token_count']}")
        print(f"     - Preview: {chunk['chunk_text'][:120]}...")

# Create structured DataFrame for easy access
chunks_df = pd.DataFrame([
    {
        'chunk_id': c['chunk_id'],
        'paper_id': c['paper_id'],
        'paper_title': c['paper_title'],
        'position': c['position'],
        'token_count': c['token_count'],
        'chunk_text': c['chunk_text']
    }
    for c in all_text_chunks
])

print(f"\n\n{'='*80}")
print("CHUNK SEGMENTATION SUMMARY")
print('='*80)
print(f"✅ Total papers processed: {len(processed_papers)}")
print(f"✅ Total chunks created: {len(all_text_chunks)}")
print(f"✅ Average chunks per paper: {len(all_text_chunks) / len(processed_papers):.1f}")
print(f"✅ Average tokens per chunk: {sum(c['token_count'] for c in all_text_chunks) / len(all_text_chunks):.1f}")
print(f"\n📊 Structured DataFrame shape: {chunks_df.shape}")
print('='*80)

# Display sample of the structured output
print("\n" + "="*80)
print("SAMPLE STRUCTURED TEXT CHUNKS (First 3)")
print("="*80)
print(chunks_df.head(3).to_string(index=False))
print("\n✅ Clean, tokenized text chunks ready for embedding!")
print("="*80)
