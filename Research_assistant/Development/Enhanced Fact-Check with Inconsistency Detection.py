import json
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

print("=" * 80)
print("ENHANCED FACT-CHECK AGENT WITH INCONSISTENCY DETECTION")
print("=" * 80)

def enhanced_fact_check_agent(summarization_data, original_papers, knowledge_base, tfidf_vectorizer):
    """
    Enhanced Fact-Check Agent that cross-references claims across multiple sources,
    identifies inconsistencies, and flags potential hallucinations using vector 
    similarity and reasoning.
    
    Args:
        summarization_data: Output from Summarization Agent
        original_papers: Original paper data for validation
        knowledge_base: Vector embeddings of paper chunks
        tfidf_vectorizer: Trained TF-IDF vectorizer
    
    Returns:
        Enhanced fact-check results with confidence scores and inconsistency flags
    """
    print(f"\n🔍 Starting Enhanced Fact-Check Agent...")
    print(f"Received data from: {summarization_data['agent']}")
    print(f"Validating {summarization_data['papers_summarized']} summaries")
    print(f"Cross-referencing across {len(knowledge_base)} knowledge base chunks\n")
    
    enhanced_fact_check = {
        'agent': 'Enhanced Fact-Check',
        'timestamp': datetime.now().isoformat(),
        'input_agent': summarization_data['agent'],
        'papers_validated': summarization_data['papers_summarized'],
        'cross_referenced_sources': len(knowledge_base),
        'validated_claims': []
    }
    
    # Create lookup for original papers
    original_papers_map = {i+1: paper for i, paper in enumerate(original_papers)}
    
    for summary in summarization_data['summaries']:
        print(f"\n{'─' * 80}")
        print(f"🔎 Fact-checking Paper {summary['paper_id']}: {summary['title'][:50]}...")
        
        original_paper = original_papers_map[summary['paper_id']]
        
        # STEP 1: Verify topics against original keywords
        claimed_topics = set(summary['key_topics'])
        actual_keywords = set(original_paper['keywords'])
        topics_match = claimed_topics.issubset(actual_keywords)
        topic_overlap_ratio = len(claimed_topics.intersection(actual_keywords)) / len(claimed_topics) if claimed_topics else 0
        
        # STEP 2: Cross-reference summary points across all sources using vector similarity
        cross_reference_results = []
        inconsistency_flags = []
        
        for point_idx, summary_point in enumerate(summary['summary_points']):
            # Vectorize the claim
            point_embedding = tfidf_vectorizer.transform([summary_point]).toarray()
            
            # Calculate similarity with all knowledge base chunks
            kb_embeddings = np.array([k['embedding'] for k in knowledge_base])
            similarities = cosine_similarity(point_embedding, kb_embeddings)[0]
            
            # Get top 3 most similar sources
            top_indices = np.argsort(similarities)[::-1][:3]
            supporting_sources = []
            
            for idx in top_indices:
                kb_entry = knowledge_base[idx]
                supporting_sources.append({
                    'paper_id': kb_entry['paper_id'],
                    'paper_title': kb_entry['paper_title'],
                    'similarity_score': float(similarities[idx]),
                    'chunk_id': kb_entry['chunk_id']
                })
            
            # Calculate confidence based on similarity scores
            max_similarity = supporting_sources[0]['similarity_score']
            avg_similarity = np.mean([s['similarity_score'] for s in supporting_sources])
            
            # Determine if claim is well-supported
            confidence_score = max_similarity
            
            # Flag potential hallucinations or inconsistencies
            is_hallucination = False
            is_inconsistent = False
            hallucination_reason = None
            
            # Check 1: Low similarity to any source (potential hallucination)
            if max_similarity < 0.15:
                is_hallucination = True
                hallucination_reason = "Low similarity to all sources - claim may not be grounded in papers"
                inconsistency_flags.append(f"Claim '{summary_point[:50]}...' has weak source support")
            
            # Check 2: Source is primarily from different paper (cross-contamination)
            primary_source_id = supporting_sources[0]['paper_id']
            if primary_source_id != summary['paper_id'] and max_similarity > 0.2:
                is_inconsistent = True
                hallucination_reason = f"Claim primarily matches Paper {primary_source_id}, not source Paper {summary['paper_id']}"
                inconsistency_flags.append(f"Cross-contamination: Claim from Paper {summary['paper_id']} matches Paper {primary_source_id}")
            
            # Check 3: Large variance in similarity scores (conflicting sources)
            similarity_variance = np.var([s['similarity_score'] for s in supporting_sources])
            if similarity_variance > 0.03:
                is_inconsistent = True
                inconsistency_flags.append(f"High variance in source support for claim '{summary_point[:50]}...'")
            
            cross_reference_results.append({
                'claim': summary_point,
                'claim_index': point_idx + 1,
                'confidence_score': round(confidence_score, 4),
                'max_similarity': round(max_similarity, 4),
                'avg_similarity': round(avg_similarity, 4),
                'supporting_sources': supporting_sources,
                'hallucination_flag': is_hallucination,
                'inconsistency_flag': is_inconsistent,
                'flag_reason': hallucination_reason
            })
            
            print(f"   Claim {point_idx + 1}: Confidence {confidence_score:.4f} | "
                  f"Hallucination: {is_hallucination} | Inconsistent: {is_inconsistent}")
        
        # STEP 3: Calculate aggregate confidence and validation status
        avg_confidence = np.mean([cr['confidence_score'] for cr in cross_reference_results])
        hallucination_count = sum(cr['hallucination_flag'] for cr in cross_reference_results)
        inconsistency_count = sum(cr['inconsistency_flag'] for cr in cross_reference_results)
        
        # Determine overall validation status
        if hallucination_count > 0:
            validation_status = "HALLUCINATION_DETECTED"
        elif inconsistency_count > 0:
            validation_status = "INCONSISTENT"
        elif avg_confidence > 0.25 and topic_overlap_ratio == 1.0:
            validation_status = "VERIFIED"
        elif avg_confidence > 0.15:
            validation_status = "PARTIAL"
        else:
            validation_status = "UNVERIFIED"
        
        validated_claim = {
            'paper_id': summary['paper_id'],
            'title': summary['title'],
            'validation_status': validation_status,
            'confidence_score': round(avg_confidence, 4),
            'topic_overlap_ratio': round(topic_overlap_ratio, 4),
            'topics_verified': topics_match,
            'claimed_topics': list(claimed_topics),
            'actual_keywords': list(actual_keywords),
            'cross_reference_results': cross_reference_results,
            'hallucination_flags': hallucination_count,
            'inconsistency_flags': inconsistency_count,
            'inconsistency_details': inconsistency_flags,
            'total_claims_checked': len(summary['summary_points'])
        }
        
        enhanced_fact_check['validated_claims'].append(validated_claim)
        
        print(f"   ✓ Overall Status: {validation_status}")
        print(f"   ✓ Confidence Score: {avg_confidence:.4f}")
        print(f"   ✓ Hallucination Flags: {hallucination_count}")
        print(f"   ✓ Inconsistency Flags: {inconsistency_count}")
    
    # Calculate aggregate metrics
    total_claims = sum(vc['total_claims_checked'] for vc in enhanced_fact_check['validated_claims'])
    total_hallucinations = sum(vc['hallucination_flags'] for vc in enhanced_fact_check['validated_claims'])
    total_inconsistencies = sum(vc['inconsistency_flags'] for vc in enhanced_fact_check['validated_claims'])
    avg_confidence = np.mean([vc['confidence_score'] for vc in enhanced_fact_check['validated_claims']])
    
    verified_count = sum(1 for vc in enhanced_fact_check['validated_claims'] if vc['validation_status'] == 'VERIFIED')
    
    enhanced_fact_check['validation_metrics'] = {
        'total_papers_validated': len(enhanced_fact_check['validated_claims']),
        'total_claims_checked': total_claims,
        'fully_verified_papers': verified_count,
        'papers_with_hallucinations': sum(1 for vc in enhanced_fact_check['validated_claims'] if vc['hallucination_flags'] > 0),
        'papers_with_inconsistencies': sum(1 for vc in enhanced_fact_check['validated_claims'] if vc['inconsistency_flags'] > 0),
        'total_hallucination_flags': total_hallucinations,
        'total_inconsistency_flags': total_inconsistencies,
        'average_confidence_score': round(avg_confidence, 4),
        'verification_rate': round(verified_count / len(enhanced_fact_check['validated_claims']), 4)
    }
    
    print(f"\n{'=' * 80}")
    print(f"✅ Enhanced Fact-Check Agent Complete")
    print(f"   • Papers validated: {len(enhanced_fact_check['validated_claims'])}")
    print(f"   • Total claims checked: {total_claims}")
    print(f"   • Fully verified: {verified_count}")
    print(f"   • Hallucination flags: {total_hallucinations}")
    print(f"   • Inconsistency flags: {total_inconsistencies}")
    print(f"   • Average confidence: {avg_confidence:.4f}")
    print(f"=" * 80)
    
    return enhanced_fact_check

# Execute Enhanced Fact-Check Agent
enhanced_fact_check_result = enhanced_fact_check_agent(
    summarization_output, 
    sample_papers, 
    knowledge_base, 
    tfidf_vectorizer
)

print(f"\n\n📊 ENHANCED FACT-CHECK OUTPUT SUMMARY")
print(f"{'=' * 80}")
print(json.dumps({
    'agent': enhanced_fact_check_result['agent'],
    'validation_metrics': enhanced_fact_check_result['validation_metrics'],
    'timestamp': enhanced_fact_check_result['timestamp']
}, indent=2))

print(f"\n\n🎯 DETAILED VALIDATION RESULTS BY PAPER")
print(f"{'=' * 80}")
for claim in enhanced_fact_check_result['validated_claims']:
    print(f"\n📄 Paper {claim['paper_id']}: {claim['title'][:60]}...")
    print(f"   Status: {claim['validation_status']}")
    print(f"   Confidence: {claim['confidence_score']:.4f}")
    print(f"   Hallucination Flags: {claim['hallucination_flags']}")
    print(f"   Inconsistency Flags: {claim['inconsistency_flags']}")
    if claim['inconsistency_details']:
        print(f"   Issues:")
        for issue in claim['inconsistency_details']:
            print(f"      - {issue}")

print(f"\n\n💾 Data structure ready: 'enhanced_fact_check_result'")
print(f"   Keys: {list(enhanced_fact_check_result.keys())}")
print(f"\n✅ SUCCESS: Fact-Check Agent with confidence scores and inconsistency flags complete!")
