import time
import hmac
import hashlib
import requests
import json
from urllib.parse import urlencode

class BybitTrader:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        
        # URLs d'API
        if testnet:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"
    
    def _generate_signature(self, payload):
        param_str = urlencode(payload)
        signature = hmac.new(
            bytes(self.api_secret, "utf-8"),
            bytes(param_str, "utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def get_market_data(self, symbol):
        endpoint = "/v2/public/tickers"
        params = {'symbol': symbol}
        
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        return response.json()
    
    def place_order(self, symbol, side, order_type, qty, price=None, take_profit=None, stop_loss=None):
        endpoint = "/v2/private/order/create"
        
        timestamp = int(time.time() * 1000)
        params = {
            'api_key': self.api_key,
            'timestamp': timestamp,
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'qty': qty
        }
        
        if price:
            params['price'] = price
        
        if take_profit:
            params['take_profit'] = take_profit
            
        if stop_loss:
            params['stop_loss'] = stop_loss
        
        # Générer la signature
        params['sign'] = self._generate_signature(params)
        
        # Envoyer l'ordre
        url = self.base_url + endpoint
        response = requests.post(url, params=params)
        return response.json()