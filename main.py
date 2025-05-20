if __name__ == "__main__":
    # Remplacez par vos clés API Bybit
    API_KEY = "votre_api_key"
    API_SECRET = "votre_api_secret"
    
    # Chemin vers votre modèle entraîné
    MODEL_PATH = "trading_patterns_model.pt"
    
    # Initialiser et démarrer le système
    trading_system = TradingSystem(API_KEY, API_SECRET, MODEL_PATH)
    trading_system.start()