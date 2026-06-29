import os

def entorno_variable(request):
    return {
        'API_INVERTIR_TEXTO_URL': os.environ.get('API_INVERTIR_TEXTO_URL', ''),
        'API_VOZ_PASIVA_URL': os.environ.get('API_VOZ_PASIVA_URL', ''), 
        'API_WORD_REPETITION_URL': os.environ.get('API_WORD_REPETITION_URL', ''),
        'API_IMPERSONAL_SENTENCES_URL': os.environ.get('API_IMPERSONAL_SENTENCES_URL', ''),
        'API_NEGATIVE_PHRASE_URL': os.environ.get('API_NEGATIVE_PHRASE_URL', ''),
        'API_OPINION_PERCEPTION_URL': os.environ.get('API_OPINION_PERCEPTION_URL', ''),
        'API_UNUSUAL_PUNCTUATION_URL': os.environ.get('API_UNUSUAL_PUNCTUATION_URL', ''),
        'API_ABSTRACT_WORDS_URL': os.environ.get('API_ABSTRACT_WORDS_URL', ''), 
        'API_LOGICAL_CONNECTORS_URL': os.environ.get('API_LOGICAL_CONNECTORS_URL', ''), 
        'API_READABILITY_METRIC_URL': os.environ.get('API_READABILITY_METRIC_URL', ''),
        'API_TENSES_URL': os.environ.get('API_TENSES_URL', ''), 
        'API_CLICHES_URL': os.environ.get('API_CLICHES_URL', '')
        




    }