import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Zerve Design System Colors
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
print("INSIGHT VISUALIZATION DASHBOARD")
print("=" * 80)

# ============================================================================
# Chart 1: Trend Analysis - Identified Research Trends
# ============================================================================
print("\n📊 Creating Chart 1: Research Trends Analysis...")

trends_fig = plt.figure(figsize=(14, 6), facecolor=BACKGROUND)
trends_ax = trends_fig.add_subplot(111, facecolor=BACKGROUND)

trends = insight_generator_output['trend_analysis']['identified_trends']
trend_names = [t['trend'] for t in trends]
trend_counts = list(range(len(trends), 0, -1))  # Priority ordering

colors_trends = [ZERVE_BLUE, ZERVE_ORANGE, ZERVE_GREEN, ZERVE_CORAL][:len(trends)]

bars_trends = trends_ax.barh(trend_names, trend_counts, color=colors_trends, edgecolor=PRIMARY_TEXT, linewidth=1.5)

trends_ax.set_xlabel('Priority Ranking', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
trends_ax.set_title('Identified Research Trends Analysis', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
trends_ax.tick_params(axis='x', colors=PRIMARY_TEXT, labelsize=10)
trends_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=11)
trends_ax.spines['bottom'].set_color(SECONDARY_TEXT)
trends_ax.spines['left'].set_color(SECONDARY_TEXT)
trends_ax.spines['top'].set_visible(False)
trends_ax.spines['right'].set_visible(False)
trends_ax.invert_yaxis()

# Add value labels
for bar in bars_trends:
    width = bar.get_width()
    trends_ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'Rank {int(width)}',
                   ha='left', va='center', color=PRIMARY_TEXT, fontsize=10, fontweight='bold')

plt.tight_layout()
print("✓ Chart 1 complete: Research trends visualized")

# ============================================================================
# Chart 2: Gap Analysis - Coverage and Missing Topics
# ============================================================================
print("\n📊 Creating Chart 2: Gap Analysis Coverage...")

gap_fig = plt.figure(figsize=(12, 7), facecolor=BACKGROUND)
gap_ax = gap_fig.add_subplot(111, facecolor=BACKGROUND)

gap_data = insight_generator_output['gap_analysis']
coverage_rate = gap_data['coverage_rate'] * 100
missing_rate = (1 - gap_data['coverage_rate']) * 100

categories = ['Topics Covered', 'Topics Missing']
values = [coverage_rate, missing_rate]
colors_gap = [SUCCESS, WARNING]

bars_gap = gap_ax.bar(categories, values, color=colors_gap, edgecolor=PRIMARY_TEXT, linewidth=2, width=0.5)

gap_ax.set_ylabel('Percentage (%)', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
gap_ax.set_title('Research Gap Analysis: Topic Coverage', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
gap_ax.tick_params(axis='x', colors=PRIMARY_TEXT, labelsize=11)
gap_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=10)
gap_ax.spines['bottom'].set_color(SECONDARY_TEXT)
gap_ax.spines['left'].set_color(SECONDARY_TEXT)
gap_ax.spines['top'].set_visible(False)
gap_ax.spines['right'].set_visible(False)
gap_ax.set_ylim(0, 100)

# Add percentage labels on bars
for bar, value in zip(bars_gap, values):
    height = bar.get_height()
    gap_ax.text(bar.get_x() + bar.get_width()/2, height + 2,
                f'{value:.1f}%',
                ha='center', va='bottom', color=PRIMARY_TEXT, fontsize=14, fontweight='bold')

# Add text annotation
gap_ax.text(0.5, 85, f"{len(gap_data['missing_topics'])} critical topics missing", 
            ha='center', fontsize=11, color=WARNING, style='italic', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor=BACKGROUND, edgecolor=WARNING, linewidth=2))

plt.tight_layout()
print("✓ Chart 2 complete: Gap analysis coverage visualized")

# ============================================================================
# Chart 3: Research Gap Severity Distribution
# ============================================================================
print("\n📊 Creating Chart 3: Research Gap Severity...")

severity_fig = plt.figure(figsize=(12, 6), facecolor=BACKGROUND)
severity_ax = severity_fig.add_subplot(111, facecolor=BACKGROUND)

gaps = gap_data['identified_gaps']
gap_types = [g['gap_type'] for g in gaps]
severity_map = {'High': 3, 'Medium-High': 2.5, 'Medium': 2, 'Low': 1}
severity_values = [severity_map.get(g['severity'], 2) for g in gaps]

severity_colors = []
for g in gaps:
    if 'High' in g['severity']:
        severity_colors.append(WARNING)
    elif 'Medium' in g['severity']:
        severity_colors.append(ZERVE_ORANGE)
    else:
        severity_colors.append(ZERVE_GREEN)

bars_severity = severity_ax.barh(gap_types, severity_values, color=severity_colors, 
                                  edgecolor=PRIMARY_TEXT, linewidth=1.5)

severity_ax.set_xlabel('Severity Level', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
severity_ax.set_title('Research Gap Severity Analysis', fontsize=16, color=PRIMARY_TEXT, fontweight='bold', pad=20)
severity_ax.tick_params(axis='x', colors=PRIMARY_TEXT, labelsize=10)
severity_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=10)
severity_ax.spines['bottom'].set_color(SECONDARY_TEXT)
severity_ax.spines['left'].set_color(SECONDARY_TEXT)
severity_ax.spines['top'].set_visible(False)
severity_ax.spines['right'].set_visible(False)
severity_ax.set_xlim(0, 3.5)

# Add severity labels
for bar, gap in zip(bars_severity, gaps):
    width = bar.get_width()
    severity_ax.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                     gap['severity'],
                     ha='left', va='center', color=PRIMARY_TEXT, fontsize=10, fontweight='bold')

# Create legend
legend_elements = [
    mpatches.Patch(facecolor=WARNING, edgecolor=PRIMARY_TEXT, label='High Severity'),
    mpatches.Patch(facecolor=ZERVE_ORANGE, edgecolor=PRIMARY_TEXT, label='Medium Severity'),
    mpatches.Patch(facecolor=ZERVE_GREEN, edgecolor=PRIMARY_TEXT, label='Low Severity')
]
severity_ax.legend(handles=legend_elements, loc='lower right', facecolor=BACKGROUND, 
                   edgecolor=SECONDARY_TEXT, labelcolor=PRIMARY_TEXT, fontsize=10)

plt.tight_layout()
print("✓ Chart 3 complete: Gap severity distribution visualized")

# ============================================================================
# Chart 4: Paper Contribution Types and Maturity
# ============================================================================
print("\n📊 Creating Chart 4: Paper Contribution Analysis...")

contrib_fig = plt.figure(figsize=(14, 6), facecolor=BACKGROUND)
contrib_ax = contrib_fig.add_subplot(111, facecolor=BACKGROUND)

comparative = insight_generator_output['comparative_findings']
contribution_types = comparative['by_contribution_type']
maturity_dist = comparative['by_maturity_level']

# Count papers by type
contrib_names = list(contribution_types.keys())
contrib_counts = [len(papers) for papers in contribution_types.values()]

x_pos = range(len(contrib_names))
colors_contrib = [ZERVE_BLUE, ZERVE_CORAL, ZERVE_GREEN, ZERVE_LAVENDER][:len(contrib_names)]

bars_contrib = contrib_ax.bar(x_pos, contrib_counts, color=colors_contrib, 
                               edgecolor=PRIMARY_TEXT, linewidth=2, width=0.6)

contrib_ax.set_xlabel('Contribution Type', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
contrib_ax.set_ylabel('Number of Papers', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
contrib_ax.set_title('Research Contribution Type Distribution', fontsize=16, color=PRIMARY_TEXT, 
                      fontweight='bold', pad=20)
contrib_ax.set_xticks(x_pos)
contrib_ax.set_xticklabels(contrib_names, fontsize=10, color=PRIMARY_TEXT, rotation=15, ha='right')
contrib_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=10)
contrib_ax.spines['bottom'].set_color(SECONDARY_TEXT)
contrib_ax.spines['left'].set_color(SECONDARY_TEXT)
contrib_ax.spines['top'].set_visible(False)
contrib_ax.spines['right'].set_visible(False)

# Add count labels
for bar, count in zip(bars_contrib, contrib_counts):
    height = bar.get_height()
    contrib_ax.text(bar.get_x() + bar.get_width()/2, height + 0.05,
                    f'{count}',
                    ha='center', va='bottom', color=PRIMARY_TEXT, fontsize=12, fontweight='bold')

plt.tight_layout()
print("✓ Chart 4 complete: Contribution types visualized")

# ============================================================================
# Chart 5: Future Research Directions by Priority
# ============================================================================
print("\n📊 Creating Chart 5: Future Research Directions...")

future_fig = plt.figure(figsize=(14, 8), facecolor=BACKGROUND)
future_ax = future_fig.add_subplot(111, facecolor=BACKGROUND)

future_dirs = insight_generator_output['future_research_directions']
dir_names = [d['direction'][:40] + '...' if len(d['direction']) > 40 else d['direction'] 
             for d in future_dirs]

# Priority scoring
priority_score_map = {'High': 3, 'Medium-High': 2.5, 'Medium': 2, 'Low': 1}
priority_scores = [priority_score_map.get(d['priority'], 2) for d in future_dirs]

# Color by priority
priority_colors = []
for d in future_dirs:
    if 'High' in d['priority']:
        priority_colors.append(HIGHLIGHT)
    elif 'Medium' in d['priority']:
        priority_colors.append(ZERVE_ORANGE)
    else:
        priority_colors.append(ZERVE_GREEN)

bars_future = future_ax.barh(dir_names, priority_scores, color=priority_colors,
                              edgecolor=PRIMARY_TEXT, linewidth=1.5)

future_ax.set_xlabel('Priority Score', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
future_ax.set_title('Future Research Directions (Prioritized)', fontsize=16, color=PRIMARY_TEXT, 
                     fontweight='bold', pad=20)
future_ax.tick_params(axis='x', colors=PRIMARY_TEXT, labelsize=10)
future_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=9)
future_ax.spines['bottom'].set_color(SECONDARY_TEXT)
future_ax.spines['left'].set_color(SECONDARY_TEXT)
future_ax.spines['top'].set_visible(False)
future_ax.spines['right'].set_visible(False)
future_ax.invert_yaxis()
future_ax.set_xlim(0, 3.5)

# Add priority labels
for bar, direction in zip(bars_future, future_dirs):
    width = bar.get_width()
    future_ax.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                   direction['priority'],
                   ha='left', va='center', color=PRIMARY_TEXT, fontsize=9, fontweight='bold')

# Create legend
legend_elements_future = [
    mpatches.Patch(facecolor=HIGHLIGHT, edgecolor=PRIMARY_TEXT, label='High Priority'),
    mpatches.Patch(facecolor=ZERVE_ORANGE, edgecolor=PRIMARY_TEXT, label='Medium Priority'),
    mpatches.Patch(facecolor=ZERVE_GREEN, edgecolor=PRIMARY_TEXT, label='Low Priority')
]
future_ax.legend(handles=legend_elements_future, loc='lower right', facecolor=BACKGROUND,
                 edgecolor=SECONDARY_TEXT, labelcolor=PRIMARY_TEXT, fontsize=10)

plt.tight_layout()
print("✓ Chart 5 complete: Future research directions visualized")

# ============================================================================
# Chart 6: Topic Frequency Heatmap
# ============================================================================
print("\n📊 Creating Chart 6: Topic Frequency Analysis...")

topic_fig = plt.figure(figsize=(12, 8), facecolor=BACKGROUND)
topic_ax = topic_fig.add_subplot(111, facecolor=BACKGROUND)

topic_freq = insight_generator_output['trend_analysis']['topic_frequency_map']
sorted_topics = sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)
topics_sorted = [t[0] for t in sorted_topics]
freqs_sorted = [t[1] for t in sorted_topics]

# Color gradient based on frequency
max_freq = max(freqs_sorted)
topic_colors = []
for freq in freqs_sorted:
    if freq == max_freq:
        topic_colors.append(ZERVE_CORAL)
    elif freq >= max_freq * 0.6:
        topic_colors.append(ZERVE_ORANGE)
    else:
        topic_colors.append(ZERVE_BLUE)

bars_topic = topic_ax.barh(topics_sorted, freqs_sorted, color=topic_colors,
                            edgecolor=PRIMARY_TEXT, linewidth=1.5)

topic_ax.set_xlabel('Frequency (Papers)', fontsize=12, color=PRIMARY_TEXT, fontweight='bold')
topic_ax.set_title('Topic Frequency Across Research Corpus', fontsize=16, color=PRIMARY_TEXT,
                    fontweight='bold', pad=20)
topic_ax.tick_params(axis='x', colors=PRIMARY_TEXT, labelsize=10)
topic_ax.tick_params(axis='y', colors=PRIMARY_TEXT, labelsize=9)
topic_ax.spines['bottom'].set_color(SECONDARY_TEXT)
topic_ax.spines['left'].set_color(SECONDARY_TEXT)
topic_ax.spines['top'].set_visible(False)
topic_ax.spines['right'].set_visible(False)
topic_ax.invert_yaxis()

# Add frequency labels
for bar, freq in zip(bars_topic, freqs_sorted):
    width = bar.get_width()
    topic_ax.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                  f'{int(freq)}',
                  ha='left', va='center', color=PRIMARY_TEXT, fontsize=9, fontweight='bold')

# Create legend
legend_elements_topic = [
    mpatches.Patch(facecolor=ZERVE_CORAL, edgecolor=PRIMARY_TEXT, label='Most Frequent'),
    mpatches.Patch(facecolor=ZERVE_ORANGE, edgecolor=PRIMARY_TEXT, label='Moderate Frequency'),
    mpatches.Patch(facecolor=ZERVE_BLUE, edgecolor=PRIMARY_TEXT, label='Low Frequency')
]
topic_ax.legend(handles=legend_elements_topic, loc='lower right', facecolor=BACKGROUND,
                edgecolor=SECONDARY_TEXT, labelcolor=PRIMARY_TEXT, fontsize=10)

plt.tight_layout()
print("✓ Chart 6 complete: Topic frequency analysis visualized")

# ============================================================================
# Summary Statistics
# ============================================================================
print(f"\n{'=' * 80}")
print("INSIGHT VISUALIZATION SUMMARY")
print("=" * 80)
print(f"✓ Charts created: 6")
print(f"✓ Trends visualized: {len(trends)}")
print(f"✓ Research gaps identified: {len(gaps)}")
print(f"✓ Future directions: {len(future_dirs)}")
print(f"✓ Topics analyzed: {len(topic_freq)}")
print(f"✓ Coverage rate: {coverage_rate:.1f}%")
print("=" * 80)