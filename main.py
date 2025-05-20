from scrabble_layout import create_scrabble_layout
from scrabble_board import generate_scrabble_board_image
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()
app.title = "Sentiment Bot API"
app.version = "0.1.0"

SCRABBLE_SCORES = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1,
    "F": 4, "G": 2, "H": 4, "I": 1, "J": 8,
    "K": 5, "L": 1, "M": 3, "N": 1, "O": 1,
    "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1,
    "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4,
    "Z": 10
}

def is_word_in_sowpods(word: str, sowpods_path: str = "sowpods.txt") -> bool:
    """
    Check if a word is present in the sowpods.txt file.

    Args:
        word (str): The word to check.
        sowpods_path (str): Path to the sowpods.txt file.

    Returns:
        bool: True if the word is present, False otherwise.
    """
    word = word.strip().upper()
    with open(sowpods_path, "r") as f:
        for line in f:
            if line.strip().upper() == word:
                return True
    return False

def score_word(word: str) -> int:
    if is_word_in_sowpods(word):
        return sum(SCRABBLE_SCORES.get(char.upper(), 0) for char in word)
    return 0

def score_words(words: list[str]) -> list[dict]:

    scored = [
        {"word": word, "score": score_word(word) }
        for word in words
    ]
    return sorted(scored, key=lambda x: x["score"], reverse=True)

class ScrabbleRequest(BaseModel):
    words: list[str]

@app.post("/scrabble")
def get_scrabble_board(request: ScrabbleRequest):
    """
    Endpoint to generate and return a Scrabble board image.
    """
    scrabble_layout = create_scrabble_layout(request.words)
    output_file = "scrabble_board.png"
    generate_scrabble_board_image(scrabble_layout, "scrabble_tiles", output_file)
    return FileResponse(output_file, media_type="image/png", filename="scrabble_board.png")

class ScoreRequest(BaseModel):
    words: list[str]

@app.post("/score")
def get_score(request: ScoreRequest):
    """
    Endpoint to return the scores of the Scrabble words, ordered highest first.
    """
    scored_words = score_words(request.words)
    return {"results": scored_words}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
