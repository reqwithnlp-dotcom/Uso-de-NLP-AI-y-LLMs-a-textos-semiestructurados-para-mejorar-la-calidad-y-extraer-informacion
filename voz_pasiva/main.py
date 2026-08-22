from detector import is_passive, passive_positions

sentence = input("Ingrese una oración en inglés: ")

if is_passive(sentence):
    print("✅ La oración está en voz pasiva")
else:
    print("❌ La oración NO está en voz pasiva")

print("Posiciones detectadas:")
print(passive_positions(sentence))