from scrabble_layout import create_scrabble_layout
from scrabble_board import generate_scrabble_board_image
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from word_validation import filter_valid_words

app = FastAPI()
app.title = "Scrabble Board Generator"
app.description = "Generate a Scrabble board image from a list of words."
app.version = "0.1.0"

SCRABBLE_SCORES = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1,
    "F": 4, "G": 2, "H": 4, "I": 1, "J": 8,
    "K": 5, "L": 1, "M": 3, "N": 1, "O": 1,
    "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1,
    "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4,
    "Z": 10
}

def score_word(word: str) -> int:
    return sum(SCRABBLE_SCORES.get(char.upper(), 0) for char in word)

def score_words(words: list[str]) -> list[dict]:
    valid_set = set(filter_valid_words(words))
    scored = [
        {"word": word, "score": score_word(word) if word in valid_set else 0}
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
