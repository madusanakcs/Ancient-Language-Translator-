import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

from sinhala_character_predictor import SinhalaCharacterPredictor

class EraPredictor:
    def __init__(self):
        self.character_predictor = SinhalaCharacterPredictor()

    def load_image(self, path):
        img = Image.open(path).convert('RGB')
        #img = ImageOps.expand(img, border=30, fill='white')  # padding
        img = img.resize((224, 224))  # resizing
        return img

    def predict_era(self, image_path):
        # Step 1: Predict the Sinhala character
        rf_label, et_label, xgb_label = self.character_predictor.predict(image_path)

        # Step 2: Use majority voting to decide final character prediction
        predictions = [rf_label, et_label, xgb_label]
        final_char = max(set(predictions), key=predictions.count)

        # Step 3: Get class ID (used in model filename)
        inv_class_map = {v: k for k, v in self.character_predictor.corrected_class_map.items()}
        if final_char not in inv_class_map:
            print(f"Character '{final_char}' not found in class map.")
            return None
        class_id = inv_class_map[final_char]

        # Step 4: Load the corresponding era model and label encoder
        try:
            model = load_model(f'Models/Eras_Models/model_{class_id}.h5')
            label_encoder = joblib.load(f'Models/Eras_Models/label_encoder_{class_id}.pkl')
        except Exception as e:
            print(f"Error loading model or label encoder for class ID {class_id}: {e}")
            return None

        # Step 5: Preprocess the image for era prediction using load_image
        img = self.load_image(image_path)
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Step 6: Predict era
        preds = model.predict(img_array, verbose=0)
        predicted_class_index = np.argmax(preds, axis=1)[0]
        predicted_era = label_encoder.inverse_transform([predicted_class_index])[0]

        # Step 7: Display and return
        print(f"\n📜 Predicted Character: {final_char}")
        print(f"🏺 Predicted Era: {predicted_era}")

        plt.imshow(img)
        plt.title(f"Era: {predicted_era}")
        plt.axis('off')
        plt.show()

        return predicted_era, final_char
