import json
from datetime import datetime

print("=" * 80)
print("AGENT 3: FACT-CHECK")
print("=" * 80)

def fact_check_agent(summarization_data, original_papers):
    """
    Agent 3: Fact-Check Agent
    Validates claims in summaries against original paper data.
    
    Args:
        summarization_data: Output from Summarization Agent
        original_papers: Original paper data for validation
    
    Returns:
        Fact-checked summaries with validation results
    """
    print(f"\n🔍 Starting Fact-Check Agent...")
    print(f"Received data from: {summarization_data['agent']}")
    print(f"Validating {summarization_data['papers_summarized']} summaries\n")
    
    fact_check_output = {
        'agent': 'Fact-Check',
        'timestamp': datetime.now().isoformat(),
        'input_agent': summarization_data['agent'],
        'papers_validated': summarization_data['papers_summarized'],
        'validated_summaries': []
    }
    
    # Create lookup for original papers
    original_papers_map = {i+1: paper for i, paper in enumerate(original_papers)}
    
    for summary in summarization_data['summaries']:
        print(f"\n{'─' * 80}")
        print(f"🔎 Fact-checking Paper {summary['paper_id']}: {summary['title'][:50]}...")
        
        original_paper = original_papers_map[summary['paper_id']]
        
        # Fact-check key topics against original keywords
        claimed_topics = set(summary['key_topics'])
        actual_keywords = set(original_paper['keywords'])
        topics_verified = claimed_topics.issubset(actual_keywords)
        
        # Verify summary points are from abstract
        abstract_text = original_paper['abstract'].lower()
        summary_verified = all(
            any(word in abstract_text for word in point.lower().split()[:3])
            for point in summary['summary_points']
        )
        
        # Calculate verification confidence
        topic_overlap = len(claimed_topics.intersection(actual_keywords)) / len(claimed_topics) if claimed_topics else 0
        
        validation_result = {
            'paper_id': summary['paper_id'],
            'title': summary['title'],
            'topics_verified': topics_verified,
            'summary_verified': summary_verified,
            'topic_overlap_ratio': round(topic_overlap, 4),
            'relevance_score': summary['relevance_score'],
            'verification_status': 'VERIFIED' if (topics_verified and summary_verified) else 'PARTIAL',
            'claimed_topics': list(claimed_topics),
            'actual_keywords': list(actual_keywords),
            'validation_notes': []
        }
        
        # Add validation notes
        if not topics_verified:
            validation_result['validation_notes'].append("Some claimed topics not in original keywords")
        if not summary_verified:
            validation_result['validation_notes'].append("Summary points may be paraphrased")
        if topic_overlap == 1.0:
            validation_result['validation_notes'].append("Perfect topic alignment with original")
        
        fact_check_output['validated_summaries'].append(validation_result)
        
        print(f"   ✓ Topics verified: {topics_verified}")
        print(f"   ✓ Summary verified: {summary_verified}")
        print(f"   ✓ Topic overlap: {topic_overlap:.2%}")
        print(f"   ✓ Status: {validation_result['verification_status']}")
    
    # Calculate aggregate validation metrics
    verified_count = sum(1 for v in fact_check_output['validated_summaries'] if v['verification_status'] == 'VERIFIED')
    avg_overlap = sum(v['topic_overlap_ratio'] for v in fact_check_output['validated_summaries']) / len(fact_check_output['validated_summaries'])
    
    fact_check_output['validation_metrics'] = {
        'total_validated': len(fact_check_output['validated_summaries']),
        'fully_verified': verified_count,
        'partially_verified': len(fact_check_output['validated_summaries']) - verified_count,
        'average_topic_overlap': round(avg_overlap, 4),
        'verification_rate': round(verified_count / len(fact_check_output['validated_summaries']), 4)
    }
    
    print(f"\n{'=' * 80}")
    print(f"✅ Fact-Check Agent Complete")
    print(f"   • Summaries validated: {len(fact_check_output['validated_summaries'])}")
    print(f"   • Fully verified: {verified_count}")
    print(f"   • Verification rate: {fact_check_output['validation_metrics']['verification_rate']:.2%}")
    print(f"=" * 80)
    
    return fact_check_output

# Execute Fact-Check Agent
fact_check_output = fact_check_agent(summarization_output, sample_papers)

print(f"\n\n📊 FACT-CHECK OUTPUT SUMMARY")
print(f"{'=' * 80}")
print(json.dumps({
    'agent': fact_check_output['agent'],
    'papers_validated': fact_check_output['papers_validated'],
    'validation_metrics': fact_check_output['validation_metrics'],
    'timestamp': fact_check_output['timestamp']
}, indent=2))

print(f"\n💾 Data structure ready for next agent: 'fact_check_output'")
print(f"   Keys: {list(fact_check_output.keys())}")
