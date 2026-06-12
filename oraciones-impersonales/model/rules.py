

from model.lexicons import (
    WEATHER_VERBS,
    WEATHER_ADJECTIVES,
    REPORTING_VERBS,
    COPULAR_VERBS,
)
from model.helpers import (
    find_subject_it,
    find_existential_there,
    has_extraposed_clause,
    get_acomp_or_attr,
)


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



RULES = (
    rule_there_existential,
    rule_weather_it,
    rule_weather_adjective,
    rule_impersonal_passive,
    rule_it_extraposition,
)

# Etiqueta por defecto cuando ninguna regla matchea
DEFAULT_TYPE = "PERSONAL"
