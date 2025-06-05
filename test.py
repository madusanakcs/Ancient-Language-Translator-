from PIL import Image
from tensorflow.keras.applications import InceptionV3, VGG19, ResNet50, InceptionResNetV2
import random
import matplotlib.pyplot as plt
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.applications.vgg19 import preprocess_input as preprocess_vgg
from keras.preprocessing.image import img_to_array
# Load models and label encoder
rf = joblib.load('Models/Letter_Classify_Models/random_forest_model.pkl')
et = joblib.load('Models/Letter_Classify_Models/extra_trees_model.pkl')
xgb = joblib.load('Models/Letter_Classify_Models/xgboost_model.pkl')
le = joblib.load('Models/Letter_Classify_Models/label_encoder.pkl')

def extract_features(image, models):
    image = img_to_array(image)

    # Convert grayscale to RGB if needed
    if image.shape[-1] == 1:
        image = np.repeat(image, 3, axis=-1)

    image = np.expand_dims(image, axis=0)
    features = []

    for name, model in models.items():
        if name == 'vgg19':
            img = preprocess_vgg(image.copy())
        else:
            img = image / 255.0
        feat = model.predict(img, verbose=0)
        features.append(feat.flatten())

    return np.concatenate(features)


corrected_class_map = {
    0: "අ", 1: "ඉ", 2: "උ", 3: "එ", 4: "ඔ",
    5: "ක", 6: "ඛ", 7: "ග", 8: "ඝ", 9: "ච", 10: "", 11: "ජ",
    12: " ", 14: "ට", 15: "ඨ", 16: "ඩ", 17: " ", 18: "ණ",
    19: "ත", 20: "ථ", 21: "ද", 22: " ", 23: "න", 24: "ප",
    25: " ", 26: "බ", 27: "භ", 28: "ම", 29: "ය",
    30: "ර", 31: "ල", 32: "ව", 33: "ශ", 35: "ස",
    36: "හ", 37: "ගා", 38: "හා", 39: "", 40: "වි", 41: "පි",
    42: "බි", 43: "ගි", 44: "පි", 45: "මි", 46: "ණි", 47: "ශි",
    48: "යි", 49: "පු", 50: "ටු", 51: "ශු", 52: "බු", 53: "දු",
    54: "නු", 55: "රි", 56: "ශි", 57: "ති", 58: "ඩි", 59: "දි",
    60: "කි", 61: "රී", 62: "නි", 63: "ඤි", 64: "ධි", 65: "ළ",
    66: "තු", 67: "ශු", 68: "පු", 69: "රු", 70: "බු", 71: "දු",
    72: "නු", 73: "ලු", 74: "චු", 75: "ලෙ", 76: "යෙ", 77: "දෙ",
    78: "නෙ", 79: "වෙ", 80: "ශෙ", 81: "ණෙ", 82: "කෙ", 83: "චෙ",
    84: "තෙ", 85: "පො", 86: "බො", 87: "ශො", 88: "ගො"
}

def get_feature_extractors():
    models = {
        'vgg19': VGG19(weights='imagenet', include_top=False, pooling='avg'),
        'inceptionv3': InceptionV3(weights='imagenet', include_top=False, pooling='avg'),
        'resnet50': ResNet50(weights='imagenet', include_top=False, pooling='avg'),
        'inceptionresnetv2': InceptionResNetV2(weights='imagenet', include_top=False, pooling='avg')
    }
    return models
    

models = get_feature_extractors()

# Provide your image path here
pathmage = "1.jpeg"
from PIL import Image, ImageOps

def load_image(path):
    img = Image.open(path).convert('RGB')
    
    # Add 25 pixels of white padding
    img = ImageOps.expand(img, border=50, fill='white')
    
    # Resize to model input size after padding (if needed)
    img = img.resize((224, 224))
    
    return np.array(img)


img = load_image(pathmage)

# Extract features
features = extract_features(img, models).reshape(1, -1)

# Predict
rf_pred = rf.predict(features)[0]
et_pred = et.predict(features)[0]
xgb_pred = xgb.predict(features)[0]

# Decode predictions
def decode(label):
    return le.inverse_transform([label])[0] if isinstance(label, (np.integer, int, np.int64)) else label

rf_decoded = corrected_class_map.get(int(decode(rf_pred)))
et_decoded = corrected_class_map.get(int(decode(et_pred)))
xgb_decoded = corrected_class_map.get(int(decode(xgb_pred)))

# Display results
plt.imshow(img)
plt.axis('off')

plt.show()

print(f"Predictions:\nRandom Forest: {rf_decoded}\nExtra Trees: {et_decoded}\nXGBoost: {xgb_decoded}")
