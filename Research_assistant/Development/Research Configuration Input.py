# Research Configuration Input Collection System
# This block defines the input structure for downstream research agents

# Research Topic
research_topic = "artificial intelligence in healthcare"

# Research Keywords - key terms to focus the research
research_keywords = [
    "machine learning diagnostics",
    "AI medical imaging",
    "clinical decision support systems",
    "healthcare automation"
]

# Research Questions - specific questions to answer
research_questions = [
    "What are the current applications of AI in medical diagnostics?",
    "How accurate are AI systems compared to human practitioners?",
    "What are the main challenges in implementing AI in healthcare settings?"
]

# Configuration metadata
config = {
    "topic": research_topic,
    "keywords": research_keywords,
    "questions": research_questions,
    "num_keywords": len(research_keywords),
    "num_questions": len(research_questions)
}

# Display configuration summary
print("=" * 60)
print("RESEARCH CONFIGURATION SUMMARY")
print("=" * 60)
print(f"\n📋 Topic: {research_topic}")
print(f"\n🔑 Keywords ({len(research_keywords)}):")
for i, keyword in enumerate(research_keywords, 1):
    print(f"   {i}. {keyword}")

print(f"\n❓ Research Questions ({len(research_questions)}):")
for i, question in enumerate(research_questions, 1):
    print(f"   {i}. {question}")

print("\n" + "=" * 60)
print("✅ Configuration ready for downstream agents")
print("=" * 60)