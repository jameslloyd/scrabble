from scrabble_layout import create_scrabble_layout
from scrabble_board import generate_scrabble_board_image
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

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