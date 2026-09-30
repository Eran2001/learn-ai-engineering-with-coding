from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.2"


def main():
    language = input("Translate English to which language? ").strip() or "Spanish"
    messages = [
        {
            "role": "system",
            "content": f"You are a translator. Translate the user's English text to {language}. "
            "Reply with only the translation, nothing else.",
        }
    ]

    while True:
        text = input("\nEnglish (or 'quit'): ").strip()
        if text.lower() in ("quit", "exit", ""):
            break

        messages.append({"role": "user", "content": text})
        try:
            stream = client.chat.completions.create(
                model=MODEL, messages=messages, stream=True
            )
            reply = ""
            print(f"{language}: ", end="")
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                print(piece, end="", flush=True)
                reply += piece
            print()
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:  # noqa: BLE001
            print(f"Error: {e} (is Ollama running?)")
            messages.pop()


if __name__ == "__main__":
    main()
