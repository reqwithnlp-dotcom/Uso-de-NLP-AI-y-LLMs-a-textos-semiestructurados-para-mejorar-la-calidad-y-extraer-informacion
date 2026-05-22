import sys
from src.detector import AdverbDetector

def main ():
    if len(sys.argv) == 2:
        sentence = sys.argv[1]
        detector = AdverbDetector()
        output = detector.analyze_sentence(sentence)
        print (output)
    else:
        print("Debe pasarse UNA frase por parametro entre comillas")
main()