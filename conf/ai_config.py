# conf/ai_config.py

class Config:
    # AI Model Settings
    MODEL_SETTINGS = {
        'basic': {
            'context_length': 8000,
            'processing_speed': 1.2,
            'supported_languages': 25,
            'token_cost': 1000
        },
        'pro': {
            'context_length': 16000,
            'processing_speed': 0.8,
            'supported_languages': 50,
            'token_cost': 2500
        },
        'enterprise': {
            'context_length': 32000,
            'processing_speed': 0.5,
            'supported_languages': 100,
            'token_cost': 5000
        }
    }

    # NLP Processing Settings
    NLP_SETTINGS = {
        'min_confidence_score': 0.85,
        'max_token_length': 512,
        'batch_size': 32,
        'default_language': 'en'
    }

    # API Endpoints
    ENDPOINTS = {
        'wikipedia_api': 'https://en.wikipedia.org/w/api.php',
        'blockchain_node': 'http://localhost:8545',
        'fact_check_service': 'https://factcheck.wikibits.org/api/v1'
    }

    # Blockchain Settings
    BLOCKCHAIN = {
        'network_id': 1,
        'contract_address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'gas_limit': 3000000,
        'min_confirmations': 3
    }

    # Cache Settings
    CACHE = {
        'enabled': True,
        'expire_time': 3600,
        'max_size': 1000
    }