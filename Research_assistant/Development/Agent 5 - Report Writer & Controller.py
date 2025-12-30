import json
from datetime import datetime

print("=" * 80)
print("AGENT 5: REPORT WRITER & CONTROLLER")
print("=" * 80)

def report_writer_agent(insight_data, fact_check_data, summarization_data, paper_reader_data):
    """
    Agent 5: Report Writer Agent
    Generates comprehensive report from all agent outputs.
    Acts as the final coordinating agent in the workflow.
    
    Args:
        insight_data: Insights from Insight Generator Agent
        fact_check_data: Validation data from Fact-Check Agent
        summarization_data: Summary data from Summarization Agent
        paper_reader_data: Extracted data from Paper Reader Agent
    
    Returns:
        Final comprehensive research report
    """
    print(f"\n📄 Starting Report Writer Agent...")
    print(f"Received data from: {insight_data['agent']}")
    print(f"Compiling report for {insight_data['papers_analyzed']} papers\n")
    
    report_output = {
        'agent': 'Report Writer',
        'timestamp': datetime.now().isoformat(),
        'report_metadata': {
            'total_papers': insight_data['papers_analyzed'],
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'agent_pipeline': [
                paper_reader_data['agent'],
                summarization_data['agent'],
                fact_check_data['agent'],
                insight_data['agent'],
                'Report Writer'
            ]
        },
        'executive_summary': {},
        'paper_reports': [],
        'synthesis': {},
        'report_complete': False
    }
    
    print(f"{'─' * 80}")
    print(f"📋 Generating Executive Summary...")
    
    # Executive Summary
    report_output['executive_summary'] = {
        'overview': f"Analysis of {insight_data['papers_analyzed']} research papers on AI in Healthcare",
        'key_findings': [
            f"Analyzed {insight_data['papers_analyzed']} papers with {insight_data['cross_paper_insights']['total_unique_topics']} unique topics",
            f"Average semantic relevance: {insight_data['cross_paper_insights']['average_relevance']:.4f}",
            f"Verification rate: {fact_check_data['validation_metrics']['verification_rate']:.0%} - {fact_check_data['validation_metrics']['fully_verified']} papers fully verified",
            f"Topic diversity indicates comprehensive coverage of AI healthcare applications"
        ],
        'methodology': "Multi-agent analysis pipeline: Paper Reading → Summarization → Fact-Checking → Insight Generation → Report Writing"
    }
    
    print(f"   ✓ Overview generated")
    print(f"   ✓ Key findings: {len(report_output['executive_summary']['key_findings'])}")
    
    # Generate individual paper reports
    print(f"\n{'─' * 80}")
    print(f"📑 Generating Individual Paper Reports...")
    
    for paper_insight in insight_data['paper_insights']:
        paper_id = paper_insight['paper_id']
        
        # Get data from all previous agents
        summary = next(s for s in summarization_data['summaries'] if s['paper_id'] == paper_id)
        validation = next(v for v in fact_check_data['validated_summaries'] if v['paper_id'] == paper_id)
        
        paper_report = {
            'paper_id': paper_id,
            'title': paper_insight['title'],
            'verification_status': paper_insight['verification_status'],
            'relevance_score': paper_insight['relevance_score'],
            'key_topics': validation['claimed_topics'],
            'summary_points': summary['summary_points'],
            'insights': paper_insight['key_insights'],
            'research_implications': paper_insight['research_implications'],
            'quality_metrics': {
                'topic_overlap': validation['topic_overlap_ratio'],
                'verification': validation['verification_status'],
                'semantic_relevance': summary['relevance_score']
            }
        }
        
        report_output['paper_reports'].append(paper_report)
        print(f"   ✓ Report {paper_id}: {paper_insight['title'][:60]}...")
    
    # Synthesis section
    print(f"\n{'─' * 80}")
    print(f"🔗 Generating Synthesis & Recommendations...")
    
    report_output['synthesis'] = {
        'cross_cutting_themes': insight_data['cross_paper_insights']['topic_diversity'],
        'trend_analysis': insight_data['cross_paper_insights']['trend_analysis'],
        'recommendations': insight_data['cross_paper_insights']['recommendations'],
        'research_gaps': [
            "Consider longitudinal studies on AI implementation outcomes",
            "Explore interdisciplinary perspectives on AI ethics in healthcare",
            "Investigate scalability challenges in clinical deployment"
        ],
        'future_directions': [
            "Integration of multimodal AI systems for comprehensive patient assessment",
            "Development of explainable AI for clinical decision transparency",
            "Standardization of evaluation metrics across AI healthcare applications"
        ]
    }
    
    report_output['report_complete'] = True
    
    print(f"   ✓ Cross-cutting themes: {len(report_output['synthesis']['cross_cutting_themes'])} topics")
    print(f"   ✓ Trends identified: {len(report_output['synthesis']['trend_analysis'])}")
    print(f"   ✓ Recommendations: {len(report_output['synthesis']['recommendations'])}")
    
    print(f"\n{'=' * 80}")
    print(f"✅ Report Writer Agent Complete")
    print(f"   • Papers in report: {len(report_output['paper_reports'])}")
    print(f"   • Executive summary: ✓")
    print(f"   • Synthesis & recommendations: ✓")
    print(f"   • Report status: {'COMPLETE' if report_output['report_complete'] else 'INCOMPLETE'}")
    print(f"=" * 80)
    
    return report_output

# Execute Report Writer Agent (acts as controller coordinating all previous agents)
report_writer_output = report_writer_agent(
    insight_generator_output,
    fact_check_output,
    summarization_output,
    paper_reader_output
)

print(f"\n\n" + "=" * 80)
print(f"CONTROLLER ORCHESTRATION COMPLETE")
print(f"=" * 80)
print(f"\n🎯 MULTI-AGENT WORKFLOW SUMMARY")
print(f"{'─' * 80}")

agent_chain = report_writer_output['report_metadata']['agent_pipeline']
for idx, agent_name in enumerate(agent_chain, 1):
    print(f"{idx}. {agent_name}")

print(f"\n📊 FINAL REPORT OUTPUT")
print(f"{'─' * 80}")
print(json.dumps({
    'agent': report_writer_output['agent'],
    'report_complete': report_writer_output['report_complete'],
    'total_papers': report_writer_output['report_metadata']['total_papers'],
    'agent_pipeline': report_writer_output['report_metadata']['agent_pipeline'],
    'timestamp': report_writer_output['timestamp']
}, indent=2))

print(f"\n✅ All agents executed successfully with proper data handoff!")
print(f"💾 Final report available in: 'report_writer_output'")
print(f"   Keys: {list(report_writer_output.keys())}")
print("=" * 80)
