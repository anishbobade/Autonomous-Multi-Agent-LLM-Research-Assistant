import json
from datetime import datetime

print("=" * 80)
print("AGENT 2: SUMMARIZATION")
print("=" * 80)

def summarization_agent(paper_reader_data):
    """
    Agent 2: Summarization Agent
    Generates concise summaries from paper reader output.
    
    Args:
        paper_reader_data: Structured data from Paper Reader Agent
    
    Returns:
        Summarized information with key findings
    """
    print(f"\n📝 Starting Summarization Agent...")
    print(f"Received data from: {paper_reader_data['agent']}")
    print(f"Processing {paper_reader_data['papers_processed']} papers\n")
    
    summarization_output = {
        'agent': 'Summarization',
        'timestamp': datetime.now().isoformat(),
        'input_agent': paper_reader_data['agent'],
        'papers_summarized': paper_reader_data['papers_processed'],
        'summaries': []
    }
    
    for paper_info in paper_reader_data['extracted_papers']:
        print(f"\n{'─' * 80}")
        print(f"📄 Summarizing Paper {paper_info['paper_id']}: {paper_info['title'][:50]}...")
        
        # Extract key sentences from abstract
        abstract_sentences = paper_info['abstract'].split('. ')
        key_sentences = [s.strip() for s in abstract_sentences if len(s.split()) > 5][:3]
        
        # Generate summary
        summary = {
            'paper_id': paper_info['paper_id'],
            'title': paper_info['title'],
            'key_topics': paper_info['keywords'][:3],
            'summary_points': key_sentences,
            'abstract_length': paper_info['abstract_length'],
            'relevance_score': sum(chunk['similarity'] for chunk in paper_info['relevant_chunks']) / len(paper_info['relevant_chunks']),
            'top_chunk': paper_info['relevant_chunks'][0] if paper_info['relevant_chunks'] else None
        }
        
        summarization_output['summaries'].append(summary)
        
        print(f"   ✓ Key topics: {', '.join(summary['key_topics'])}")
        print(f"   ✓ Summary points: {len(summary['summary_points'])}")
        print(f"   ✓ Relevance score: {summary['relevance_score']:.4f}")
        print(f"   ✓ Top chunk ID: {summary['top_chunk']['chunk_id'] if summary['top_chunk'] else 'N/A'}")
    
    # Generate aggregate insights
    avg_relevance = sum(s['relevance_score'] for s in summarization_output['summaries']) / len(summarization_output['summaries'])
    total_topics = len(set(topic for s in summarization_output['summaries'] for topic in s['key_topics']))
    
    summarization_output['aggregate_insights'] = {
        'average_relevance': round(avg_relevance, 4),
        'unique_topics': total_topics,
        'total_summary_points': sum(len(s['summary_points']) for s in summarization_output['summaries'])
    }
    
    print(f"\n{'=' * 80}")
    print(f"✅ Summarization Agent Complete")
    print(f"   • Papers summarized: {len(summarization_output['summaries'])}")
    print(f"   • Average relevance: {avg_relevance:.4f}")
    print(f"   • Unique topics identified: {total_topics}")
    print(f"=" * 80)
    
    return summarization_output

# Execute Summarization Agent with Paper Reader output
summarization_output = summarization_agent(paper_reader_output)

print(f"\n\n📊 SUMMARIZATION OUTPUT SUMMARY")
print(f"{'=' * 80}")
print(json.dumps({
    'agent': summarization_output['agent'],
    'papers_summarized': summarization_output['papers_summarized'],
    'aggregate_insights': summarization_output['aggregate_insights'],
    'timestamp': summarization_output['timestamp']
}, indent=2))

print(f"\n💾 Data structure ready for next agent: 'summarization_output'")
print(f"   Keys: {list(summarization_output.keys())}")
