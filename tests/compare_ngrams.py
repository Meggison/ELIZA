import sys
import re
import collections
from typing import Dict, List, Tuple
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'notebooks'))
from unsmoothed_ngrams import generate_ngrams

def build_ngram_model(n: int, text: str) -> Dict[Tuple[str, ...], int]:
    """Build an unsmoothed n-gram model from the given text."""
    tokens = re.findall(r'\w+', text.lower())
    print(f"Generated {len(tokens)} tokens.")
    ngrams = generate_ngrams(n, tokens)
    return collections.Counter(ngrams)

def get_ngram_probabilities(model: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, ...], float]:
    """Convert counts to probabilities."""
    total = sum(model.values())
    return {gram: count/total for gram, count in model.items()}

def compare_corpora(file1: str, file2: str, n: int = 1) -> None:
    """Compare n-gram statistics between two corpora."""
    print(f"\nComparing {n}-grams between corpora...")
    
    # Read files
    with open(file1, 'r', encoding='utf-8') as f:
        text1 = f.read()
    with open(file2, 'r', encoding='utf-8') as f:
        text2 = f.read()
    
    print(f"\nCorpus 1 length: {len(text1)} characters")
    print(f"Corpus 2 length: {len(text2)} characters")
    
    # Build models
    print("\nProcessing Corpus 1...")
    model1 = build_ngram_model(n, text1)
    print("\nProcessing Corpus 2...")
    model2 = build_ngram_model(n, text2)
    
    # Convert to probabilities
    probs1 = get_ngram_probabilities(model1)
    probs2 = get_ngram_probabilities(model2)
    
    # Create comparison dataframe
    data = []
    all_ngrams = set(probs1.keys()) | set(probs2.keys())
    
    for ngram in all_ngrams:
        prob1 = probs1.get(ngram, 0)
        prob2 = probs2.get(ngram, 0)
        count1 = model1.get(ngram, 0)
        count2 = model2.get(ngram, 0)
        diff = abs(prob1 - prob2)
        
        data.append({
            'n-gram': ' '.join(ngram),
            'prob_corpus1': prob1,
            'count_corpus1': count1,
            'prob_corpus2': prob2,
            'count_corpus2': count2,
            'abs_diff': diff
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('abs_diff', ascending=False)
    
    # Display results
    print("\nTop 10 most different n-grams between corpora:")
    print(df.head(10).to_string(index=False, float_format=lambda x: '{:.4f}'.format(x)))
    
    print("\nTop 10 most common n-grams in Corpus 1:")
    top1 = sorted(probs1.items(), key=lambda x: x[1], reverse=True)[:10]
    for gram, prob in top1:
        print(f"{' '.join(gram)}: {prob:.4f} ({model1[gram]} occurrences)")
    
    print("\nTop 10 most common n-grams in Corpus 2:")
    top2 = sorted(probs2.items(), key=lambda x: x[1], reverse=True)[:10]
    for gram, prob in top2:
        print(f"{' '.join(gram)}: {prob:.4f} ({model2[gram]} occurrences)")

def main():
    # File paths relative to project root
    corpus1 = '../corpora_1.txt'
    corpus2 = '../corpora_2.txt'
    
    print("Comparing unigrams (n=1)...")
    compare_corpora(corpus1, corpus2, n=1)
    
    print("\nComparing bigrams (n=2)...")
    compare_corpora(corpus1, corpus2, n=2)

if __name__ == "__main__":
    main()
