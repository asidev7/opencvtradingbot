import cv2
import numpy as np

def preprocess_chart_image(image_path):
    # Chargement de l'image
    img = cv2.imread(image_path)
    
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Amélioration du contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Réduction du bruit
    denoised = cv2.GaussianBlur(enhanced, (5, 5), 0)
    
    # Détection des contours (pour figures chartistes)
    edges = cv2.Canny(denoised, 50, 150)
    
    return {
        'original': img,
        'gray': gray,
        'enhanced': enhanced,
        'edges': edges
    }