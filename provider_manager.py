from providers import ask_gemini, ask_ollama, ask_groq
from config import TALK_MODEL, MEMORY_MODEL


def ask_provider(prompt, mode="default"):

    if mode == "thinking":

        try:
            print("[GEMINI RESPONSE]")
            return ask_gemini(prompt)

        except Exception:
            print("[OLLAMA RESPONSE]")
            print(
                "\n[ERROR]: Cloud model is unable to respond! \nSwitching to local model..."
            )
            return ask_ollama(prompt, model_name=MEMORY_MODEL)

    if mode == "local":

        print("[OLLAMA RESPONSE]")
        return ask_ollama(prompt, model_name=MEMORY_MODEL)

    if mode == "cloud":
        try:
            print("[GROQ RESPONSE]")
            return ask_groq(prompt)
        except Exception:
            print("\n[ERROR]: Groq is unable to respond! Trying Gemini...")

        try:
            print("[GEMINI RESPONSE]")
            return ask_gemini(prompt)
        except Exception:
            print("\n[ERROR]: Gemini is unable to respond!")

        print("[OLLAMA RESPONSE]")
        print("[ERROR]: Cloud models failed. Switching to TALK_MODEL...")
        return ask_ollama(prompt, model_name=TALK_MODEL)

    print("[OLLAMA RESPONSE]")
    return ask_ollama(prompt, model_name=TALK_MODEL)
