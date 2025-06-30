from wordfreq import top_n_list, zipf_frequency
import random

def cargar_palabras(lang="en", top_n=50000, min_len=5, max_len=10, min_freq=3.5):
    lista = top_n_list(lang, n_top=top_n)
    return [
        w for w in lista
        if min_len <= len(w) <= max_len and zipf_frequency(w, lang) >= min_freq
    ]

def iniciar_juego():
    palabras = cargar_palabras()
    secreto = random.choice(palabras)
    return {
        "secret": secreto,
        "masked": ["_"] * len(secreto),
        "errors": 0,
        "max_errors": 5
    }

def procesar_intento(state: dict, letra: str) -> dict:
    secreto = state["secret"]
    masked = state["masked"]
    errors = state["errors"]
    if letra not in secreto:
        state["errors"] = errors + 1
    for i, c in enumerate(secreto):
        if c == letra:
            masked[i] = c
    state["masked"] = masked
    if "_" not in masked:
        state["result"] = "win"
    elif state["errors"] >= state["max_errors"]:
        state["result"] = "lose"
    return state