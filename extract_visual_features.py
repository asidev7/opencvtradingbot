def extract_visual_features(model, image_path):
    # Charger l'image prétraitée
    img = cv2.imread(image_path)
    
    # Détection avec YOLOv5
    results = model(img)
    
    # Extraction des patterns détectés
    patterns = []
    confidence_scores = []
    
    for *box, conf, cls in results.xyxy[0]:  # xyxy, confidence, class
        pattern_type = results.names[int(cls)]
        patterns.append(pattern_type)
        confidence_scores.append(float(conf))
    
    # Caractéristiques supplémentaires
    # Analyse des couleurs (bougies vertes vs rouges)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
    red_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    green_count = cv2.countNonZero(green_mask)
    red_count = cv2.countNonZero(red_mask)
    
    return {
        'detected_patterns': patterns,
        'confidence_scores': confidence_scores,
        'green_red_ratio': green_count / max(red_count, 1)
    }