import nltk
from nltk.corpus import words as nltk_words

# Download once before running (uncomment and run once)
#nltk.download('words')

ENGLISH_WORDS = set(nltk_words.words())

def is_valid_word(word: str) -> bool:
    # Check if the word is in the dictionary and not a proper noun (not capitalized)
    return word.lower() in ENGLISH_WORDS and not word[0].isupper()

def filter_valid_words(words: list[str]) -> list[str]:
    return [word for word in words if is_valid_word(word)]

if __name__ == "__main__":
    # Example usage
    words = ["hello", "world", "Python", "scrabble", "Test"]
    valid_words = filter_valid_words(words)
    print("Valid words:", valid_words)