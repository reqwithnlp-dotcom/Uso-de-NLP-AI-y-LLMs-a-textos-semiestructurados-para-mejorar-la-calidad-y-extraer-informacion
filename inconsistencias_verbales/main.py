from rules_spacy import *
import pandas as pd
import spacy


RULES = [
    detect_aux_mismatch,
    detect_subject_verb_mismatch,
    detect_temporal_mismatch,
    detect_tense_mismatch,
    detect_connector_mismatch,

]

print("Loading spaCy...")

nlp = spacy.load("en_core_web_md")


def analyze_text(text):

    doc = nlp(text)

    results = []

    for sent in doc.sents:

        sentence_errors = [0]*5

        for i,rule in enumerate(RULES):

            error = rule(sent)

            if error:
                sentence_errors[i]=1

    return sentence_errors


def create_errors_column():

    dataset = pd.read_csv("df_limpio.csv")
    for index, row in dataset.iterrows():
        text = row["Original_Sentence"]
        print(text)
        error_vector = analyze_text(text)
        for i, error in enumerate(error_vector):
            dataset.at[index, f"rule_{i+1}"] = error
    
    dataset.to_csv("df_1_with_errors.csv", index=False)


def limpiarDf():
    df = pd.read_csv("prueba1Mezcla.csv")

    columna = "Original_Sentence"

    df = df[
        df[columna].apply(
            lambda x: isinstance(x, str) and x.strip() != ""
        )
    ]

    df.to_csv("df_limpio.csv", index=False)



create_errors_column()