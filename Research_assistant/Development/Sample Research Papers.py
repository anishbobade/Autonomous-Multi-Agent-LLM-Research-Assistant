import textwrap

# Sample research papers on AI in healthcare for NLP pipeline testing
sample_papers = [
    {
        "title": "Deep Learning in Medical Image Analysis: Recent Advances and Future Directions",
        "abstract": """
        This comprehensive review examines the application of deep learning techniques in medical image analysis. 
        Convolutional Neural Networks (CNNs) have revolutionized the field, achieving diagnostic accuracy comparable 
        to expert radiologists in multiple domains. Recent studies demonstrate that AI systems can detect diabetic 
        retinopathy with 95% sensitivity and 98% specificity. However, challenges remain in clinical integration, 
        including interpretability, regulatory approval, and workflow optimization. This paper synthesizes current 
        evidence and proposes future research directions for machine learning in diagnostic imaging.
        """,
        "keywords": ["deep learning", "medical imaging", "CNN", "diagnostics", "healthcare AI"]
    },
    {
        "title": "Clinical Decision Support Systems: A Meta-Analysis of Effectiveness",
        "abstract": """
        Clinical Decision Support Systems (CDSS) powered by artificial intelligence are transforming healthcare delivery. 
        Our meta-analysis of 127 randomized controlled trials reveals that AI-augmented CDSS improve diagnostic accuracy 
        by 23% on average and reduce medical errors by 37%. Machine learning models trained on electronic health records 
        can predict patient deterioration 24-48 hours before clinical manifestation. Despite promising results, implementation 
        barriers include data privacy concerns, algorithm bias, and physician resistance to technology adoption. 
        Future work must address these challenges while maintaining patient safety and care quality.
        """,
        "keywords": ["clinical decision support", "machine learning", "healthcare automation", "patient safety"]
    },
    {
        "title": "Natural Language Processing for Electronic Health Records: Applications and Challenges",
        "abstract": """
        Natural Language Processing (NLP) techniques are increasingly applied to extract structured information from 
        unstructured clinical notes. State-of-the-art transformer models like BERT and GPT achieve F1 scores above 0.90 
        for named entity recognition of medical concepts. NLP systems can automatically identify adverse drug events, 
        extract treatment outcomes, and support clinical research. However, challenges persist including medical jargon 
        variability, abbreviation ambiguity, and the need for domain-specific training data. This review discusses current 
        NLP architectures, evaluation metrics, and future directions for clinical text mining.
        """,
        "keywords": ["natural language processing", "electronic health records", "text mining", "BERT", "medical NLP"]
    }
]

# Display sample papers
print("=" * 80)
print("SAMPLE RESEARCH PAPERS FOR NLP PIPELINE")
print("=" * 80)
print(f"\n📚 Total Papers: {len(sample_papers)}\n")

for idx, paper in enumerate(sample_papers, 1):
    print(f"\n{idx}. {paper['title']}")
    print("-" * 80)
    print(f"Keywords: {', '.join(paper['keywords'])}")
    print(f"\nAbstract Preview (first 200 chars):")
    print(textwrap.fill(paper['abstract'].strip()[:200] + "...", width=80))
    print()

print("=" * 80)
print("✅ Sample papers ready for NLP processing")
print("=" * 80)
