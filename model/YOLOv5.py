# Entraînement
from ultralytics import YOLO

# Charger le modèle
model = YOLO('yolov5s.pt')  # Modèle pré-entraîné

# Entraîner sur vos données
results = model.train(
    data='path/to/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# Sauvegarde
model.save('trading_patterns_model.pt')