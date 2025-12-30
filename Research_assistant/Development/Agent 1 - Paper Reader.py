import json
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 80)
print("AGENT 1: PAPER READER")
print("=" * 80)

# Agent 1: Paper Reader - Extracts and structures paper content
def paper_reader_agent(papers, search_function):
    """
    Agent 1: Paper Reader
    Reads and extracts key information from research papers.
    
    Args:
        papers: List of paper dictionaries with title, abstract, keywords
        search_function: Semantic search function for finding relevant chunks
    
    Returns:
        Structured data with extracted paper information
    """
    print("\n📚 Starting Paper Reader Agent...")
    print(f"Processing {len(papers)} research papers\n")
    
    paper_reader_output = {
        'agent': 'Paper Reader',
        'timestamp': datetime.now().isoformat(),
        'papers_processed': len(papers),
        'extracted_papers': []
    }
    
    for idx, paper in enumerate(papers):
        print(f"\n{'─' * 80}")
        print(f"📄 Paper {idx + 1}: {paper['title'][:60]}...")
        
        # Extract key information
        paper_info = {
            'paper_id': idx + 1,
            'title': paper['title'],
            'abstract': paper['abstract'].strip(),
            'keywords': paper['keywords'],
            'abstract_length': len(paper['abstract'].strip().split()),
            'keyword_count': len(paper['keywords'])
        }
        
        # Perform semantic search for each paper's keywords
        search_query = ' '.join(paper['keywords'][:3])
        relevant_chunks = search_function(search_query, top_k=2)
        
        paper_info['relevant_chunks'] = [{
            'chunk_id': chunk['chunk_id'],
            'similarity': round(chunk['similarity'], 4),
            'text_preview': chunk['chunk_text'][:100]
        } for chunk in relevant_chunks]
        
        paper_reader_output['extracted_papers'].append(paper_info)
        
        print(f"   ✓ Title: {paper['title']}")
        print(f"   ✓ Abstract words: {paper_info['abstract_length']}")
        print(f"   ✓ Keywords: {', '.join(paper['keywords'][:3])}")
        print(f"   ✓ Found {len(relevant_chunks)} relevant chunks")
    
    print(f"\n{'=' * 80}")
    print(f"✅ Paper Reader Agent Complete")
    print(f"   • Papers processed: {len(papers)}")
    print(f"   • Total keywords extracted: {sum(p['keyword_count'] for p in paper_reader_output['extracted_papers'])}")
    print(f"=" * 80)
    
    return paper_reader_output

# Execute Paper Reader Agent
paper_reader_output = paper_reader_agent(sample_papers, semantic_search)

print(f"\n\n📊 PAPER READER OUTPUT SUMMARY")
print(f"{'=' * 80}")
print(json.dumps({
    'agent': paper_reader_output['agent'],
    'papers_processed': paper_reader_output['papers_processed'],
    'timestamp': paper_reader_output['timestamp']
}, indent=2))

print(f"\n💾 Data structure ready for next agent: 'paper_reader_output'")
print(f"   Keys: {list(paper_reader_output.keys())}")
