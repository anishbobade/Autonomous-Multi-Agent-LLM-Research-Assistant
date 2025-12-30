import matplotlib.pyplot as plt
import numpy as np

# Zerve design system colors
BACKGROUND = '#1D1D20'
PRIMARY_TEXT = '#fbfbff'
SECONDARY_TEXT = '#909094'
ZERVE_BLUE = '#A1C9F4'
ZERVE_ORANGE = '#FFB482'
ZERVE_GREEN = '#8DE5A1'
ZERVE_CORAL = '#FF9F9B'
ZERVE_LAVENDER = '#D0BBFF'
HIGHLIGHT = '#ffd400'
SUCCESS = '#17b26a'
WARNING = '#f04438'

print("=" * 80)
print("FACT-CHECK VISUALIZATION DASHBOARD")
print("=" * 80)

metrics = enhanced_fact_check_result['validation_metrics']

# Figure 1: Validation Status Distribution
validation_fig = plt.figure(figsize=(10, 6), facecolor=BACKGROUND)
ax1 = validation_fig.add_subplot(111, facecolor=BACKGROUND)

status_counts = {}
for claim in enhanced_fact_check_result['validated_claims']:
    status = claim['validation_status']
    status_counts[status] = status_counts.get(status, 0) + 1

statuses = list(status_counts.keys())
counts = list(status_counts.values())
colors = [SUCCESS if s == 'VERIFIED' else WARNING if s == 'HALLUCINATION_DETECTED' else ZERVE_ORANGE for s in statuses]

bars = ax1.bar(statuses, counts, color=colors, edgecolor=PRIMARY_TEXT, linewidth=1.5, alpha=0.85)
ax1.set_title('Paper Validation Status Distribution', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
ax1.set_xlabel('Validation Status', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax1.set_ylabel('Number of Papers', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax1.tick_params(colors=PRIMARY_TEXT, labelsize=10)
ax1.spines['bottom'].set_color(SECONDARY_TEXT)
ax1.spines['left'].set_color(SECONDARY_TEXT)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', color=PRIMARY_TEXT, fontsize=11, fontweight='bold')

plt.tight_layout()
print("\n✅ Figure 1: Validation Status Distribution created")

# Figure 2: Confidence Scores by Paper
confidence_fig = plt.figure(figsize=(12, 6), facecolor=BACKGROUND)
ax2 = confidence_fig.add_subplot(111, facecolor=BACKGROUND)

paper_ids = [f"Paper {c['paper_id']}" for c in enhanced_fact_check_result['validated_claims']]
confidence_scores = [c['confidence_score'] for c in enhanced_fact_check_result['validated_claims']]
bar_colors = [SUCCESS if c['validation_status'] == 'VERIFIED' else 
              WARNING if c['validation_status'] == 'HALLUCINATION_DETECTED' else 
              ZERVE_ORANGE for c in enhanced_fact_check_result['validated_claims']]

bars2 = ax2.bar(paper_ids, confidence_scores, color=bar_colors, edgecolor=PRIMARY_TEXT, linewidth=1.5, alpha=0.85)
ax2.axhline(y=metrics['average_confidence_score'], color=HIGHLIGHT, linestyle='--', linewidth=2, 
            label=f"Average: {metrics['average_confidence_score']:.4f}")

ax2.set_title('Confidence Scores by Paper', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
ax2.set_xlabel('Paper', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax2.set_ylabel('Confidence Score', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax2.set_ylim([0, 0.5])
ax2.tick_params(colors=PRIMARY_TEXT, labelsize=10)
ax2.spines['bottom'].set_color(SECONDARY_TEXT)
ax2.spines['left'].set_color(SECONDARY_TEXT)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Add value labels on bars
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.4f}',
             ha='center', va='bottom', color=PRIMARY_TEXT, fontsize=10, fontweight='bold')

legend = ax2.legend(loc='upper right', facecolor=BACKGROUND, edgecolor=SECONDARY_TEXT, fontsize=10)
for text in legend.get_texts():
    text.set_color(PRIMARY_TEXT)

plt.tight_layout()
print("✅ Figure 2: Confidence Scores by Paper created")

# Figure 3: Hallucination and Inconsistency Flags
flags_fig = plt.figure(figsize=(10, 6), facecolor=BACKGROUND)
ax3 = flags_fig.add_subplot(111, facecolor=BACKGROUND)

x_positions = np.arange(len(paper_ids))
width = 0.35

hallucination_flags = [c['hallucination_flags'] for c in enhanced_fact_check_result['validated_claims']]
inconsistency_flags = [c['inconsistency_flags'] for c in enhanced_fact_check_result['validated_claims']]

bars3a = ax3.bar(x_positions - width/2, hallucination_flags, width, label='Hallucination Flags',
                 color=WARNING, edgecolor=PRIMARY_TEXT, linewidth=1.5, alpha=0.85)
bars3b = ax3.bar(x_positions + width/2, inconsistency_flags, width, label='Inconsistency Flags',
                 color=ZERVE_ORANGE, edgecolor=PRIMARY_TEXT, linewidth=1.5, alpha=0.85)

ax3.set_title('Hallucination and Inconsistency Flags by Paper', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
ax3.set_xlabel('Paper', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax3.set_ylabel('Number of Flags', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax3.set_xticks(x_positions)
ax3.set_xticklabels(paper_ids)
ax3.tick_params(colors=PRIMARY_TEXT, labelsize=10)
ax3.spines['bottom'].set_color(SECONDARY_TEXT)
ax3.spines['left'].set_color(SECONDARY_TEXT)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Add value labels on bars
for bars in [bars3a, bars3b]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}',
                     ha='center', va='bottom', color=PRIMARY_TEXT, fontsize=10, fontweight='bold')

legend = ax3.legend(loc='upper right', facecolor=BACKGROUND, edgecolor=SECONDARY_TEXT, fontsize=10)
for text in legend.get_texts():
    text.set_color(PRIMARY_TEXT)

plt.tight_layout()
print("✅ Figure 3: Hallucination and Inconsistency Flags created")

# Figure 4: Overall Validation Metrics Summary
summary_fig = plt.figure(figsize=(10, 7), facecolor=BACKGROUND)
ax4 = summary_fig.add_subplot(111, facecolor=BACKGROUND)

metric_labels = [
    'Total Papers',
    'Fully Verified',
    'Papers with\nInconsistencies',
    'Papers with\nHallucinations',
    'Total Claims\nChecked'
]

metric_values = [
    metrics['total_papers_validated'],
    metrics['fully_verified_papers'],
    metrics['papers_with_inconsistencies'],
    metrics['papers_with_hallucinations'],
    metrics['total_claims_checked']
]

metric_colors = [ZERVE_BLUE, SUCCESS, ZERVE_ORANGE, WARNING, ZERVE_LAVENDER]

bars4 = ax4.barh(metric_labels, metric_values, color=metric_colors, edgecolor=PRIMARY_TEXT, linewidth=1.5, alpha=0.85)

ax4.set_title('Overall Validation Metrics Summary', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
ax4.set_xlabel('Count', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax4.tick_params(colors=PRIMARY_TEXT, labelsize=11)
ax4.spines['bottom'].set_color(SECONDARY_TEXT)
ax4.spines['left'].set_color(SECONDARY_TEXT)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars4, metric_values)):
    ax4.text(value + 0.1, bar.get_y() + bar.get_height()/2.,
             f'{int(value)}',
             ha='left', va='center', color=PRIMARY_TEXT, fontsize=11, fontweight='bold')

plt.tight_layout()
print("✅ Figure 4: Overall Validation Metrics Summary created")

# Figure 5: Claim-Level Confidence Distribution
claim_confidence_fig = plt.figure(figsize=(12, 6), facecolor=BACKGROUND)
ax5 = claim_confidence_fig.add_subplot(111, facecolor=BACKGROUND)

all_claim_confidences = []
claim_labels = []
for claim in enhanced_fact_check_result['validated_claims']:
    for cross_ref in claim['cross_reference_results']:
        all_claim_confidences.append(cross_ref['confidence_score'])
        claim_labels.append(f"P{claim['paper_id']}-C{cross_ref['claim_index']}")

colors_by_confidence = [SUCCESS if c >= 0.4 else ZERVE_ORANGE if c >= 0.25 else WARNING for c in all_claim_confidences]

bars5 = ax5.bar(range(len(all_claim_confidences)), all_claim_confidences, color=colors_by_confidence,
                edgecolor=PRIMARY_TEXT, linewidth=1.2, alpha=0.85)

ax5.axhline(y=0.4, color=SUCCESS, linestyle=':', linewidth=1.5, alpha=0.5, label='High Confidence (≥0.40)')
ax5.axhline(y=0.25, color=ZERVE_ORANGE, linestyle=':', linewidth=1.5, alpha=0.5, label='Medium Confidence (≥0.25)')
ax5.axhline(y=0.15, color=WARNING, linestyle=':', linewidth=1.5, alpha=0.5, label='Hallucination Risk (<0.15)')

ax5.set_title('Individual Claim Confidence Scores', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
ax5.set_xlabel('Claim (Paper-Claim)', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax5.set_ylabel('Confidence Score', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
ax5.set_xticks(range(len(claim_labels)))
ax5.set_xticklabels(claim_labels, rotation=45, ha='right')
ax5.tick_params(colors=PRIMARY_TEXT, labelsize=9)
ax5.spines['bottom'].set_color(SECONDARY_TEXT)
ax5.spines['left'].set_color(SECONDARY_TEXT)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

legend = ax5.legend(loc='upper right', facecolor=BACKGROUND, edgecolor=SECONDARY_TEXT, fontsize=9)
for text in legend.get_texts():
    text.set_color(PRIMARY_TEXT)

plt.tight_layout()
print("✅ Figure 5: Individual Claim Confidence Scores created")

print("\n" + "=" * 80)
print("📊 DASHBOARD SUMMARY")
print("=" * 80)
print(f"✅ 5 visualizations created")
print(f"✅ All figures use Zerve design system")
print(f"✅ Key Insights:")
print(f"   • {metrics['fully_verified_papers']} of {metrics['total_papers_validated']} papers fully verified")
print(f"   • {metrics['total_hallucination_flags']} hallucination flags detected")
print(f"   • {metrics['total_inconsistency_flags']} inconsistency flags detected")
print(f"   • Average confidence score: {metrics['average_confidence_score']:.4f}")
print(f"   • Verification rate: {metrics['verification_rate']:.2%}")
print("=" * 80)
