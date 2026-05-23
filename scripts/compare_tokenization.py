import os
import time
import json
import nltk
import tiktoken
from transformers import AutoTokenizer


def run_comparison():
    # Ensure docs directory exists
    os.makedirs("../docs", exist_ok=True)

    try:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
    except:
        pass

    with open("../data/resume.txt", "r", encoding="utf-8") as f:
        text = f.read()

    tokenizers_to_test = {
        "Tiktoken (cl100k_base - OpenAI)": lambda t: len(
            tiktoken.get_encoding("cl100k_base").encode(t)
        ),
        "HuggingFace (gpt2)": lambda t: len(
            AutoTokenizer.from_pretrained("gpt2").encode(t)
        ),
        "NLTK (Word Tokenize)": lambda t: len(nltk.word_tokenize(t)),
    }

    text_length = len(text)
    results = {"original_text_length_chars": text_length, "tokenizers": {}}

    for name, tokenize_fn in tokenizers_to_test.items():
        try:
            start_time = time.time()
            # Run multiple times for stable timing
            for _ in range(10):
                token_count = tokenize_fn(text)
            encoding_time = (time.time() - start_time) / 10

            ratio = token_count / text_length

            results["tokenizers"][name] = {
                "token_count": token_count,
                "tokens_per_character": ratio,
                "encoding_speed_seconds": encoding_time,
            }
        except Exception as e:
            results["tokenizers"][name] = {"error": str(e)}

    with open("../docs/tokenizer_strategy.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(
        "Tokenization comparison complete. Results saved to ../docs/tokenizer_strategy.json"
    )


if __name__ == "__main__":
    run_comparison()
