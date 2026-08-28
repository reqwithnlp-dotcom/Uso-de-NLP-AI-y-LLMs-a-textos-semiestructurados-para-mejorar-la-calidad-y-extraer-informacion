import spacy


def test_tokens():
    """
    Test function that tokenizes an English sentence and creates
    a dictionary where each token's POS tag is the key and its text
    is the value.
    """

    nlp = spacy.load("en_core_web_md")

    sentence = "I am leaving tomorrow."

    doc = nlp(sentence)

    tokens = {}

    for token in doc:
        tokens[token.pos_] = token.text

    print("Dictionary:")
    print(tokens["VERB"])

    print("\nTokens:")
    for key, value in tokens.items():
        print(f"POS: {key} | Text: {value}")


if __name__ == "__main__":
    test_tokens()