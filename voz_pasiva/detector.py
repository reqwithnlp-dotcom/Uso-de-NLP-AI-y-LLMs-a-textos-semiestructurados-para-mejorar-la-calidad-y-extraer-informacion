import spacy

# Carga del modelo de inglés
nlp = spacy.load("en_core_web_sm")

def is_passive(sentence):
   #transforma la oracion en objeto doc con tokens y anotaciones
    doc = nlp(sentence)

    #recoro la oracion
    for token in doc:
        if token.dep_ == "auxpass": #busco auxiliar pasivo
            return True   #si encuentra alguno de los auxiliares was, were, is, been

    return False

#Devuelve posiciones inicial y final de los auxiliares pasivos, los muestra en una tupla
# El parametro es la oracion
def passive_positions(sentence):
    #transforma la oracion en objeto doc con tokens y anotaciones
    doc = nlp(sentence)

    results = []
    #recoro la oracion
    for token in doc:

        # Busca auxiliar pasivo
        if token.dep_ == "auxpass":

            start = token.idx
            end = token.idx + len(token.text)

            # intenta extender hasta el participio pasado ,
            for child in token.head.children:
                if child.tag_ == "VBN":
                    end = child.idx + len(child.text)

            results.append((start, end))

    return results