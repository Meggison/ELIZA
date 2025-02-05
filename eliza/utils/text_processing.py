from typing import List, Union, Pattern
import re
from pathlib import Path
import functools

# Cache compiled patterns
ALPHA_PATTERN = re.compile(r"[a-zA-Z]+")
WORD_START_PATTERN = re.compile(r'^[A-Za-z]+')

@functools.lru_cache(maxsize=128)
def compile_pattern(pattern: str) -> Pattern:
    """Compile and cache regex patterns."""
    return re.compile(pattern)

def load_corpus_text(filepath: Union[str, Path] = "shakes.txt", 
                    lines: bool = False, 
                    raw: bool = False) -> Union[str, List[str]]:
    """
    Loads text from a file and returns it as raw text, lines, or words.
    
    Args:
        filepath: Path to the text file
        lines: If True, split text into lines
        raw: If True, return raw text
        
    Returns:
        Text as string or list depending on parameters
    
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {e}")
    
    if raw:
        return text
    elif lines:
        return text.splitlines()
    return text.split()

def get_alphabetic_strings(file_path: Union[str, Path] = "shakes.txt") -> List[str]:
    """Returns a list of words that contain only alphabetic characters."""
    text = load_corpus_text(file_path)
    return [word for word in text if ALPHA_PATTERN.fullmatch(word)]

def get_alphabetic_strings_lower(file_path: Union[str, Path] = "shakes.txt", 
                               ending: str = "b") -> List[str]:
    """Returns a list of lowercase words ending with a specified letter."""
    text = load_corpus_text(file_path)
    pattern = compile_pattern(fr"^[a-z]+{ending}$")
    return [word.lower() for word in text if pattern.fullmatch(word.lower())]

def get_alphabet_words_pair(file_path: Union[str, Path] = "shakes.txt", 
                          preceding: str = "a", 
                          following: str = "b") -> List[str]:
    """Finds words that start with a specified preceding letter and end with a specified following letter."""
    text = load_corpus_text(file_path)
    pattern = compile_pattern(fr"^{preceding}[a-zA-Z]*{following}$")
    return [word for word in text if pattern.match(word)]

def consecutive_repeated_words(file_path: Union[str, Path] = "shakes.txt") -> List[str]:
    """Finds lines with consecutive repeated words."""
    text = load_corpus_text(file_path, lines=True)
    pattern = compile_pattern(r"(\b\w+\b)\s+\1\b")
    return [line for line in text if pattern.search(line)]

def integer_start_word_end(file_path: Union[str, Path] = "shakes.txt", 
                         max_lines: int = 500) -> List[str]:
    """
    Finds lines that start with a number and end with a word.
    
    Args:
        file_path: Path to the text file
        max_lines: Maximum number of lines to process
        
    Returns:
        List of matching lines
    """
    text = load_corpus_text(file_path, lines=True)
    pattern = compile_pattern(r"^[0-9]+(\b.*\b)+[A-Za-z]+$")
    return [line for line in text[:max_lines] if pattern.match(line)]

def find_words(file_path: Union[str, Path] = "shakes.txt", 
              words: tuple = ("raven", "raven")) -> List[str]:
    """
    Finds lines containing specified words.
    
    Args:
        file_path: Path to the text file
        words: Tuple of words to search for
        
    Returns:
        List of lines containing the specified words
    """
    text = load_corpus_text(file_path, lines=True)
    pattern = compile_pattern(fr"\b({'|'.join(words)})\b.*\b({'|'.join(words)})*\b")
    return [line for line in text if pattern.search(line)]

def capture_first_word(file_path: Union[str, Path] = "shakes.txt") -> List[str]:
    """Captures the first word in each line using pre-compiled pattern."""
    text = load_corpus_text(file_path, lines=True)
    return [WORD_START_PATTERN.match(line).group() 
            for line in text 
            if WORD_START_PATTERN.match(line)]

def capture_first_word_punc(file_path: Union[str, Path] = "shakes.txt") -> List[str]:
    """Extracts words from text, ignoring punctuation."""
    text = load_corpus_text(file_path, lines=True, raw=True)
    words = re.split(r'[^\w\s]', text)
    return [word.strip() for word in words if word.strip()]

if __name__ == "__main__":
    try:
        # Test all functions with error handling
        shakespare_text = load_corpus_text()
        print("First 10 words:", shakespare_text[:10])
        
        print("\nTesting various word patterns:")
        for func in [
            get_alphabetic_strings,
            lambda: get_alphabetic_strings_lower(ending='b'),
            lambda: get_alphabet_words_pair(preceding='a', following='b'),
            consecutive_repeated_words,
            integer_start_word_end,
            lambda: find_words(words=('raven', 'raven')),
            capture_first_word
        ]:
            try:
                result = func()[:5]  # Get first 5 results
                print(f"\n{func.__name__}:", result)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                
    except Exception as e:
        print(f"Error during testing: {e}")