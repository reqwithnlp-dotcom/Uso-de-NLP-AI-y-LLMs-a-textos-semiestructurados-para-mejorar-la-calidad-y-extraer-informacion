

from model.lexicons import (
    WEATHER_VERBS,
    WEATHER_ADJECTIVES,
    REPORTING_VERBS,
    COPULAR_VERBS,
    PERSONAL_PRONOUNS,
    AMBIGUOUS_SUBJECTS,
)
from model.helpers import (
    find_subject_it,
    find_existential_there,
    has_extraposed_clause,
    get_acomp_or_attr,
    find_root,
    get_subject,
)


# ===========================================================================
# Reglas IMPERSONALES: evidencia de oración impersonal.
# Devuelven un subtipo (str) si matchean, o None.
# ===========================================================================


def rule_there_existential(sent):

    there = find_existential_there(sent)
    if there is not None and there.head.lemma_ == "be":
        return "THERE_EXISTENTIAL"
    return None


def rule_weather_it(sent):
    it = find_subject_it(sent)
    if it is not None and it.head.lemma_ in WEATHER_VERBS:
        return "WEATHER_IT"
    return None


def rule_weather_adjective(sent):
   
    it = find_subject_it(sent)
    if it is None or it.head.lemma_ not in COPULAR_VERBS:
        return None
    adj = get_acomp_or_attr(it.head)
    if adj is not None and adj.lemma_.lower() in WEATHER_ADJECTIVES:
        return "WEATHER_ADJECTIVE"
    return None


def rule_impersonal_passive(sent):
    
    it = find_subject_it(sent)
    if it is None:
        return None
    head = it.head


    if head.tag_ == "VBN" and head.lemma_ in REPORTING_VERBS:
        if has_extraposed_clause(head):
            return "IMPERSONAL_PASSIVE"

  
    if head.lemma_ == "be":
        for child in head.children:
            if child.tag_ == "VBN" and child.lemma_ in REPORTING_VERBS:
                if has_extraposed_clause(child) or has_extraposed_clause(head):
                    return "IMPERSONAL_PASSIVE"
    return None


def rule_it_extraposition(sent):
  
    it = find_subject_it(sent)
    if it is None or it.head.lemma_ not in COPULAR_VERBS:
        return None
    verb = it.head

    adj = get_acomp_or_attr(verb)
    if adj is not None and (has_extraposed_clause(adj) or has_extraposed_clause(verb)):
        return "IT_EXTRAPOSITION"

   
    if verb.lemma_ in ("seem", "appear", "happen", "turn") and has_extraposed_clause(verb):
        return "IT_EXTRAPOSITION"
    return None



IMPERSONAL_RULES = (
    rule_there_existential,
    rule_weather_it,
    rule_weather_adjective,
    rule_impersonal_passive,
    rule_it_extraposition,
)


# ===========================================================================
# Reglas PERSONALES: evidencia POSITIVA de sujeto referencial.
# Devuelven un subtipo (str) si detectan rasgo personal, o None.
#
# Diseño: miran SIEMPRE el sujeto de la raíz (ROOT), no cualquier sujeto de
# la oración. Así "It is known that I was late" no se marca personal por el
# "I" subordinado: su raíz es el pasivo impersonal con sujeto "It".
# ===========================================================================

def rule_personal_pronoun_subject(sent):
    """Sujeto raíz = pronombre personal referencial (I/you/he/she/we/they)."""
    subj = get_subject(find_root(sent))
    if subj is not None and subj.lower_ in PERSONAL_PRONOUNS:
        return "PRONOUN_SUBJECT"
    return None


def rule_personal_nominal_subject(sent):
    """Sujeto raíz nominal real: nombre propio, sustantivo, demostrativo,
    indefinido ('someone', 'this'...) o cláusula sujeto.

    Excluye expletivos y los sujetos dudosos (it/there/one), que se dejan
    a las reglas impersonales o a la capa 2."""
    subj = get_subject(find_root(sent))
    if subj is None or subj.dep_ == "expl":
        return None
    if subj.lower_ in AMBIGUOUS_SUBJECTS or subj.lower_ in PERSONAL_PRONOUNS:
        return None
    return "NOMINAL_SUBJECT"


def rule_imperative(sent):
    """Imperativo: verbo raíz en forma base, sin sujeto explícito
    ('Open the door'). El sujeto 'you' está implícito -> oración personal."""
    root = find_root(sent)
    if root is None or root.pos_ != "VERB" or root.tag_ != "VB":
        return None
    if get_subject(root) is not None:
        return None
    return "IMPERATIVE"


PERSONAL_RULES = (
    rule_personal_pronoun_subject,
    rule_personal_nominal_subject,
    rule_imperative,
)


# Alias retrocompatible: histórico `RULES` == reglas impersonales.
RULES = IMPERSONAL_RULES

# Etiqueta por defecto del subtipo impersonal cuando ninguna regla matchea
DEFAULT_TYPE = "PERSONAL"
