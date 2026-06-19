def limpiarDf():
    df = pd.read_csv("prueba1Mezcla.csv")

    columna = "Original_Sentence"

    df = df[
        df[columna].apply(
            lambda x: isinstance(x, str) and x.strip() != ""
        )
    ]

    df.to_csv("df_limpio.csv", index=False)