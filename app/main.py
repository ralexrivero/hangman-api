from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from app.game import iniciar_juego, procesar_intento

app = FastAPI(title="Hangman API", version="1.0")

class GameState(BaseModel):
    secret: str
    masked: list[constr(min_length=1, max_length=1)]
    errors: int
    max_errors: int
    result: str | None = None

class GuessIn(BaseModel):
    state: GameState
    letter: constr(min_length=1, max_length=1)

@app.post("/start", response_model=GameState)
def api_start():
    """Inicia un nuevo juego y devuelve el estado inicial."""
    return iniciar_juego()

@app.post("/guess", response_model=GameState)
def api_guess(data: GuessIn):
    """Proces un intento de letra y devuelve el estado actualizado"""
    state = data.state.dict()
    letra = data.letter.lower()
    if state.get("result"):
        raise HTTPException(400, "El juego ya terminó")
    return procesar_intento(state, letra)
