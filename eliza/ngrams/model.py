import sys
import re
import collections
import math
from typing import List, Tuple, Dict
import argparse

def generate_ngrams(n, words):
    """Generate n-grams from a list of words."""
    print(f"Generating {n}-grams from {len(words)} words...")
    return [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]

def build_ngram_model(n, text):
    """Build an unsmoothed n-gram model (frequency count) from the given text."""
    print("Tokenizing text...")
    # Tokenize text: convert to lowercase and extract words
    tokens = re.findall(r'\w+', text.lower())
    print(f"Generated {len(tokens)} tokens.")
    ngrams = generate_ngrams(n, tokens)
    print(f"Generated {len(ngrams)} {n}-grams.")
    return collections.Counter(ngrams)

def calculate_probabilities(model: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, ...], float]:
    """Calculate probabilities from n-gram counts."""
    total = sum(model.values())
    return {ngram: count/total for ngram, count in model.items()}

def calculate_perplexity(test_text: str, model: Dict[Tuple[str, ...], int], n: int, 
                        smoothing_value: float = 1e-10) -> float:
    """
    Calculate perplexity of test_text given the n-gram model.
    Uses a small smoothing value for unseen n-grams to avoid infinite perplexity.
    
    Args:
        test_text: Text to calculate perplexity for
        model: N-gram frequency counts
        n: Size of n-grams
        smoothing_value: Small value to use for unseen n-grams
    
    Returns:
        Perplexity value
    """
    # Get probabilities from counts
    probs = calculate_probabilities(model)
    
    # Tokenize test text
    tokens = re.findall(r'\w+', test_text.lower())
    test_ngrams = generate_ngrams(n, tokens)
    
    if not test_ngrams:
        return float('inf')
    
    # Calculate log probability
    total_log_prob = 0
    total_ngrams = len(test_ngrams)
    
    for ngram in test_ngrams:
        # Use smoothing_value for unseen n-grams
        prob = probs.get(ngram, smoothing_value)
        total_log_prob += math.log2(prob)
    
    # Calculate perplexity: 2^(-1/N * sum(log2(P(wi|w1...wi-1))))
    avg_log_prob = total_log_prob / total_ngrams
    perplexity = math.pow(2, -avg_log_prob)
    
    return perplexity

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Analyze n-grams in text')
    parser.add_argument('n', type=int, nargs='?', default=2, help='Size of n-grams')
    parser.add_argument('--file', '-f', type=str, help='Input file (default: stdin)')
    args = parser.parse_args()

    # Read input
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: {args.file} not found.")
            sys.exit(1)
    else:
        # Read from stdin
        text = sys.stdin.read()

    if not text:
        print("Error: No input text provided.")
        sys.exit(1)

    print(f"Read {len(text)} characters.")
    print("Building the n-gram model...")
    
    # Split text into training (90%) and test (10%) sets
    words = re.findall(r'\w+', text.lower())
    split_point = int(len(words) * 0.9)
    train_text = ' '.join(words[:split_point])
    test_text = ' '.join(words[split_point:])
    
    # Build model on training text
    train_model = build_ngram_model(args.n, train_text)
    
    # Calculate perplexity on test text
    perplexity = calculate_perplexity(test_text, train_model, args.n)
    print(f"\nPerplexity on test set: {perplexity:.2f}")
    
    model = build_ngram_model(args.n, text)
    total = sum(model.values())
    print(f"\nTotal {args.n}-grams: {total}\n")
    
    print("Top 10 most common n-grams (unsmoothed probabilities):\n")
    probs = calculate_probabilities(model)
    for gram, count in model.most_common(10):
        prob = probs[gram]
        print(f"{gram}: {prob:.4f} ({count} occurrences)")

if __name__ == "__main__":
    main()
