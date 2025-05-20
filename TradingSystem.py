import time
import schedule
import json
import os

class TradingSystem:
    def __init__(self, bybit_api_key, bybit_api_secret, model_path, symbol="BTCUSDT"):
        # Initialisation
        self.symbol = symbol
        self.bybit = BybitTrader(bybit_api_key, bybit_api_secret)
        self.model = YOLO(model_path)
        
        # Configuration
        self.trade_amount = 0.01  # BTC
        self.take_profit_percent = 0.02  # 2%
        self.stop_loss_percent = 0.01    # 1%
        
        # État actuel
        self.position_open = False
        self.last_position_type = None  # 'long' ou 'short'
        
    def capture_and_analyze(self):
        # Capturer l'écran
        chart_image = capture_chart()
        
        # Prétraitement
        processed_images = preprocess_chart_image(chart_image)
        
        # Extraction des caractéristiques
        features = extract_visual_features(self.model, chart_image)
        
        # Obtenir les données du marché
        market_data = self.bybit.get_market_data(self.symbol)
        current_price = float(market_data['result'][0]['last_price'])
        
        return {
            'chart_image': chart_image,
            'features': features,
            'current_price': current_price
        }
    
    def trading_decision(self, analysis):
        # Logique de décision basée sur les patterns détectés
        features = analysis['features']
        patterns = features['detected_patterns']
        confidence = features['confidence_scores']
        
        # Exemple de règle simple
        signal = None
        
        if 'head_shoulders' in patterns and confidence[patterns.index('head_shoulders')] > 0.75:
            signal = 'short'
        elif 'inverse_head_shoulders' in patterns and confidence[patterns.index('inverse_head_shoulders')] > 0.75:
            signal = 'long'
        elif 'double_top' in patterns and confidence[patterns.index('double_top')] > 0.7:
            signal = 'short'
        elif 'double_bottom' in patterns and confidence[patterns.index('double_bottom')] > 0.7:
            signal = 'long'
        
        # Considérer le ratio vert/rouge pour confirmer
        if signal == 'long' and features['green_red_ratio'] < 0.8:
            signal = None  # Annuler si trop de rouge
        elif signal == 'short' and features['green_red_ratio'] > 1.2:
            signal = None  # Annuler si trop de vert
            
        return signal
    
    def execute_trade(self, signal, current_price):
        if signal == 'long':
            # Calculer TP et SL
            take_profit = current_price * (1 + self.take_profit_percent)
            stop_loss = current_price * (1 - self.stop_loss_percent)
            
            # Placer l'ordre
            order = self.bybit.place_order(
                symbol=self.symbol,
                side="Buy",
                order_type="Market",
                qty=self.trade_amount,
                take_profit=take_profit,
                stop_loss=stop_loss
            )
            
            self.position_open = True
            self.last_position_type = 'long'
            
        elif signal == 'short':
            # Calculer TP et SL
            take_profit = current_price * (1 - self.take_profit_percent)
            stop_loss = current_price * (1 + self.stop_loss_percent)
            
            # Placer l'ordre
            order = self.bybit.place_order(
                symbol=self.symbol,
                side="Sell",
                order_type="Market",
                qty=self.trade_amount,
                take_profit=take_profit,
                stop_loss=stop_loss
            )
            
            self.position_open = True
            self.last_position_type = 'short'
            
        # Journaliser le trade
        self.log_trade(signal, current_price)
    
    def log_trade(self, signal, price):
        log_entry = {
            'timestamp': time.time(),
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'signal': signal,
            'price': price,
            'position_type': self.last_position_type
        }
        
        with open('trade_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def run_iteration(self):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Exécution de l'analyse...")
        
        # Analyse du marché
        analysis = self.capture_and_analyze()
        
        # Décision de trading
        signal = self.trading_decision(analysis)
        
        # Exécuter le trade si nécessaire
        if signal and not self.position_open:
            print(f"Signal détecté: {signal} à {analysis['current_price']}")
            self.execute_trade(signal, analysis['current_price'])
        else:
            print("Pas de signal ou position déjà ouverte.")
    
    def start(self):
        # Planifier l'exécution toutes les 5 minutes
        schedule.every(5).minutes.do(self.run_iteration)
        
        # Boucle principale
        print("Système de trading démarré...")
        while True:
            schedule.run_pending()
            time.sleep(1)