import sys
import unittest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'notebooks'))

from unsmoothed_ngrams import (
    generate_ngrams,
    build_ngram_model,
    calculate_probabilities,
    calculate_perplexity
)

class TestUnsmoothedNgrams(unittest.TestCase):
    def setUp(self):
        # Simple test text
        self.test_text = "the cat in the hat"
        self.test_tokens = ["the", "cat", "in", "the", "hat"]
        
    def test_generate_ngrams(self):
        # Test unigrams
        unigrams = generate_ngrams(1, self.test_tokens)
        expected_unigrams = [('the',), ('cat',), ('in',), ('the',), ('hat',)]
        self.assertEqual(unigrams, expected_unigrams)
        
        # Test bigrams
        bigrams = generate_ngrams(2, self.test_tokens)
        expected_bigrams = [
            ('the', 'cat'),
            ('cat', 'in'),
            ('in', 'the'),
            ('the', 'hat')
        ]
        self.assertEqual(bigrams, expected_bigrams)
        
    def test_build_ngram_model(self):
        # Test bigram model building
        model = build_ngram_model(2, self.test_text)
        
        # Check counts
        self.assertEqual(model[('the', 'cat')], 1)
        self.assertEqual(model[('cat', 'in')], 1)
        self.assertEqual(model[('in', 'the')], 1)
        self.assertEqual(model[('the', 'hat')], 1)
        
        # Check total counts
        self.assertEqual(sum(model.values()), 4)  # 4 bigrams total
        
    def test_calculate_probabilities(self):
        model = build_ngram_model(1, self.test_text)
        probs = calculate_probabilities(model)
        
        # Check that probabilities sum to 1
        self.assertAlmostEqual(sum(probs.values()), 1.0)
        
        # Check specific probabilities
        # 'the' appears twice in 5 tokens
        self.assertAlmostEqual(probs[('the',)], 0.4)
        # 'cat' appears once in 5 tokens
        self.assertAlmostEqual(probs[('cat',)], 0.2)
        
    def test_calculate_perplexity(self):
        # Train on "the cat in the hat"
        train_text = self.test_text
        test_text = "the cat in the hat"  # same text, should have low perplexity
        
        model = build_ngram_model(2, train_text)
        perplexity = calculate_perplexity(test_text, model, 2)
        
        # Since test text is same as train text, perplexity should be relatively low
        self.assertLess(perplexity, 100)
        
        # Test with completely different text
        different_text = "dog runs fast"
        different_perplexity = calculate_perplexity(different_text, model, 2)
        
        # Perplexity should be higher for different text
        self.assertGreater(different_perplexity, perplexity)
        
    def test_edge_cases(self):
        # Test empty text
        empty_model = build_ngram_model(1, "")
        self.assertEqual(len(empty_model), 0)
        
        # Test single word
        single_model = build_ngram_model(1, "word")
        self.assertEqual(len(single_model), 1)
        self.assertEqual(single_model[('word',)], 1)
        
        # Test perplexity with empty test text
        model = build_ngram_model(1, self.test_text)
        perplexity = calculate_perplexity("", model, 1)
        self.assertEqual(perplexity, float('inf'))

if __name__ == '__main__':
    unittest.main()
