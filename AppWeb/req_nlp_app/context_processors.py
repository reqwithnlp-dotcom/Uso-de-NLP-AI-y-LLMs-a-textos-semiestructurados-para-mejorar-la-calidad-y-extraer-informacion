import os

def entorno_variable(request):
    return {
        'API_CLICHES_URL': os.environ.get('API_CLICHES_URL') or 'http://127.0.0.1:8001',
        'API_WORD_REPETITION_URL': os.environ.get('API_WORD_REPETITION_URL') or 'http://127.0.0.1:8002',
        'API_LOGICAL_CONNECTORS_URL': os.environ.get('API_LOGICAL_CONNECTORS_URL') or 'http://127.0.0.1:8003',
        'API_NEGATIVE_PHRASE_URL': os.environ.get('API_NEGATIVE_PHRASE_URL') or 'http://127.0.0.1:8004',
        'API_UNUSUAL_PUNCTUATION_URL': os.environ.get('API_UNUSUAL_PUNCTUATION_URL') or 'http://127.0.0.1:8005',
        'API_UNUSUAL_PUNCT_URL': os.environ.get('API_UNUSUAL_PUNCT_URL') or os.environ.get('API_UNUSUAL_PUNCTUATION_URL') or 'http://127.0.0.1:8005',
        'API_MODAL_VERBS_URL': os.environ.get('API_MODAL_VERBS_URL') or 'http://127.0.0.1:8006',
        'API_ADVERBS_URL': os.environ.get('API_ADVERBS_URL') or 'http://127.0.0.1:8007',
        'API_READABILITY_METRIC_URL': os.environ.get('API_READABILITY_METRIC_URL') or 'http://127.0.0.1:8008',
        'API_IMPERSONAL_SENTENCES_URL': os.environ.get('API_IMPERSONAL_SENTENCES_URL') or 'http://127.0.0.1:8009',
        'API_OPINION_PERCEPTION_URL': os.environ.get('API_OPINION_PERCEPTION_URL') or 'http://127.0.0.1:8010',
        'API_VOZ_PASIVA_URL': os.environ.get('API_VOZ_PASIVA_URL') or 'http://127.0.0.1:8011',
        'API_WEAK_VERBS_URL': os.environ.get('API_WEAK_VERBS_URL') or 'http://127.0.0.1:8012',
        'API_ABSTRACT_WORDS_URL': os.environ.get('API_ABSTRACT_WORDS_URL') or 'http://127.0.0.1:8013',
        'API_POVSHIFT_URL': os.environ.get('API_POVSHIFT_URL') or 'http://127.0.0.1:8014',
        'API_TENSES_URL': os.environ.get('API_TENSES_URL') or 'http://127.0.0.1:8015',
        'API_INVERTIR_TEXTO_URL': os.environ.get('API_INVERTIR_TEXTO_URL') or 'http://127.0.0.1:8000',
    }