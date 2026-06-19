from rules_spacy import *
import pandas as pd
import spacy
import numpy as np


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

    for sent in doc.sents:

        sentence_errors = [0]*5

        for i,rule in enumerate(RULES):

            error = rule(sent)

            if error:
                sentence_errors[i]=1

    return sentence_errors


def create_errors_column():

    dataset = pd.read_csv("df_limpio.csv") # toma el dataset que ya esté sin vacios y previamente con las etiquetas de error
    for index, row in dataset.iterrows():
        text = row["Original_Sentence"]
        print(text)
        error_vector = analyze_text(text)
        for i, error in enumerate(error_vector):
            dataset.at[index, f"rule_{i+1}"] = error
    
    dataset.to_csv("df_1_with_errors.csv", index=False)








def weigh_data():
    df = pd.read_csv("df_1_with_errors.csv") 
    matriz = np.zeros((2, 5))
    ultimas_6 = df.iloc[:, -6:]
    for fila_idx,fila in ultimas_6.iterrows():
        for indice,(columna, valor) in enumerate(fila.iloc[1:].items()):
            valor_referencia = fila.iloc[0]
            if valor_referencia == 1 and valor == 1.0:
                matriz[0,indice] += 1
            else:
                if valor_referencia == 0 and valor == 1.0:
                    matriz[1,indice] += 1
    print(matriz)

weigh_data()

#create_errors_column()