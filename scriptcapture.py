from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import cv2
import numpy as np
from PIL import ImageGrab
import datetime

# Configuration du navigateur
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécution en arrière-plan
driver = webdriver.Chrome(options=chrome_options)

# Connexion à TradingView (ajustez l'URL selon vos besoins)
driver.get("https://www.tradingview.com/chart/")
time.sleep(10)  # Attendre le chargement

# Fonction de capture d'écran
def capture_chart():
    # Cibler la zone du graphique (ajustez selon votre écran)
    x1, y1, x2, y2 = 200, 300, 1400, 800
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    # Conversion pour OpenCV
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Sauvegarde avec horodatage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chart_{timestamp}.png"
    cv2.imwrite(filename, screenshot)
    return filename

# Boucle de capture (toutes les 5 minutes)
while True:
    filename = capture_chart()
    print(f"Capture sauvegardée: {filename}")
    time.sleep(300)  # 5 minutes