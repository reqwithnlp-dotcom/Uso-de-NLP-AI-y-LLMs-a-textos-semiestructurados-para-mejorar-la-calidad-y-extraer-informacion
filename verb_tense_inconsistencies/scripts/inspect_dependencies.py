import spacy


nlp = spacy.load("en_core_web_md")

sentences1 = [
    # Present Simple
    "The system validates the request.",
    "The system does not validate the request.",
    #"Does the system validate the request?",

    # Present Continuous
    #"The system is validating the request.",
    #"The system is not validating the request.",
    #"Is the system validating the request?",

    # Present Perfect
    "The system has validated the request.",
    #"The system has not validated the request.",
    #"Has the system validated the request?",

    # Present Perfect Continuous
    "The system has been validating the request.",
    #"The system has not been validating the request.",
    #"Has the system been validating the request?",

    # Past Simple
    #"The system validated the request.",
    #"The system did not validate the request.",
   # "Did the system validate the request?",

    # Past Continuous
    #"The system was validating the request.",
    #"The system was not validating the request.",
    #"Was the system validating the request?",

    # Past Perfect
    #"The system had validated the request.",
    #"The system had not validated the request.",
    #"Had the system validated the request?",

    # Past Perfect Continuous
    #"The system had been validating the request.",
    #"The system had not been validating the request.",
    #"Had the system been validating the request?",

    # Future Simple
    #"The system will validate the request.",
    #"The system will not validate the request.",
    #"Will the system validate the request?",

    # Future Continuous
    #"The system will be validating the request.",
    #"The system will not be validating the request.",
    #"Will the system be validating the request?",

    # Future Perfect
    #"The system will have validated the request.",
    #"The system will not have validated the request.",
    #"Will the system have validated the request?",

    # Future Perfect Continuous
    #"The system will have been validating the request.",
    #"The system will not have been validating the request.",
    #"Will the system have been validating the request?",

    # Multiple verb phrases
    #"The user submits the request and the system validates it.",
    "The user has submitted the request and the system validates it.",
    "When the user has submitted the request, the system validates it.",
    #"The system validates the request after the user has submitted it.",
    "If the user had submitted the request, the system would have validated it.",
]

sentences2 = [
    # ============================================================
    # 1. BE / HAVE como verbos principales
    # ============================================================

    "The system is reliable.",
    "The system is not reliable.",
    "Is the system reliable?",

    "The system has a problem.",
    "The system does not have a problem.",
    "Does the system have a problem?",

    # ============================================================
    # 2. Modal verbs
    # ============================================================

    "The system must validate the request.",
    "The system must not validate the request.",
    "Must the system validate the request?",

    "The system should validate the request.",
    "The system should not validate the request.",
    "Should the system validate the request?",

    "The system would validate the request.",
    "The system would not validate the request.",
    "Would the system validate the request?",

    "The system might validate the request.",
    "The system might not validate the request.",
    "Might the system validate the request?",

    # ============================================================
    # 3. Modal + perfect
    # ============================================================

    "The system should have validated the request.",
    "The system should not have validated the request.",
    "Should the system have validated the request?",

    "The system would have validated the request.",
    "The system would not have validated the request.",
    "Would the system have validated the request?",

    # ============================================================
    # 4. Modal + continuous
    # ============================================================

    "The system should be validating the request.",
    "The system should not be validating the request.",
    "Should the system be validating the request?",

    "The system would be validating the request.",
    "The system would not be validating the request.",
    "Would the system be validating the request?",

    # ============================================================
    # 5. HAVE TO
    # ============================================================

    "The system has to validate the request.",
    "The system does not have to validate the request.",
    "Does the system have to validate the request?",

    "The system had to validate the request.",
    "The system did not have to validate the request.",
    "Did the system have to validate the request?",

    # ============================================================
    # 6. Passive voice
    # ============================================================

    "The request is validated by the system.",
    "The request is not validated by the system.",
    "Is the request validated by the system?",

    "The request was validated by the system.",
    "The request was not validated by the system.",
    "Was the request validated by the system?",

    "The request has been validated by the system.",
    "The request has not been validated by the system.",
    "Has the request been validated by the system?",

    "The request will be validated by the system.",
    "The request will not be validated by the system.",
    "Will the request be validated by the system?",

    # ============================================================
    # 7. Verb + infinitive
    # ============================================================

    "The system needs to validate the request.",
    "The system does not need to validate the request.",
    "Does the system need to validate the request?",

    "The system wants to validate the request.",
    "The system does not want to validate the request.",
    "Does the system want to validate the request?",

    # ============================================================
    # 8. Verb + gerund
    # ============================================================

    "The system started validating the request.",
    "The system did not start validating the request.",
    "Did the system start validating the request?",

    "The system stopped validating the request.",
    "The system did not stop validating the request.",
    "Did the system stop validating the request?",

    # ============================================================
    # 9. Phrasal verbs
    # ============================================================

    "The system logs in to the server.",
    "The system does not log in to the server.",
    "Does the system log in to the server?",

    "The system has shut down the service.",
    "The system has not shut down the service.",
    "Has the system shut down the service?",

    # ============================================================
    # 10. Multiple clauses
    # ============================================================

    "The user needs to submit the request and the system validates it.",

    "The user has submitted the request because the system requires it.",

    "When the user submits the request, the system validates it.",

    "If the user submits the request, the system will validate it.",

    "If the user had submitted the request, the system would have validated it.",

    # ============================================================
    # 11. Nested / complex verb phrases
    # ============================================================

    "The system should have been validating the request.",

    "The system should not have been validating the request.",

    "Should the system have been validating the request?",

    "The request should have been validated by the system.",

    "The request should not have been validated by the system.",

    "Should the request have been validated by the system?",
]

sentences3 = [
    "The system is reliable.",
    "The system has a problem.",
    "The system should validate the request.",
    "The system should have validated the request.",
    "The system should be validating the request.",

"The system has to validate the request.",
"The system does not have to validate the request.",

"The request has been validated by the system.",
"The request will be validated by the system.",

"The system needs to validate the request.",

"The user needs to submit the request and the system validates it.",

"The request should have been validated by the system.",
]

sentences4 = [
    "The system has validate the mandatory fields.",
    "The system had process all pending transactions.",
    "The monitoring service is generate diagnostic information.",
    "The system has validate the request.",
    "The system has validated the request.",
    "The system had process the transactions.",
    "The system had processed the transactions.",

    "The system is generate information.",
    "The system is generating information.",
    "The system has load all pending transactions from the repository.",
    "I have submitted the request.",
 ]   
   

def print_dependencies(doc):
    print("\nTOKENS:")
    print("-" * 90)

    for token in doc:
        print(
            f"{token.i:2} "
            f"{token.text:15} "
            f"POS={token.pos_:5} "
            f"TAG={token.tag_:5} "
            f"DEP={token.dep_:12} "
            f"HEAD={token.head.text}"
        )


def print_tree(token, level=0):
    indent = "  " * level

    print(
        f"{indent}- {token.text!r} "
        f"[POS={token.pos_}, TAG={token.tag_}, DEP={token.dep_}]"
    )

    for child in token.children:
        print_tree(child, level + 1)


for sentence in sentences4:
    print("\n" + "=" * 100)
    print(sentence)
    print("=" * 100)

    doc = nlp(sentence)

    print_dependencies(doc)

    print("\nVERB SUBTREES:")

    for token in doc:
        if token.pos_ == "VERB":
            print(f"\nMain verb candidate: {token.text!r}")
            print_tree(token)