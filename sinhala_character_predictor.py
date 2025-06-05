import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from keras.applications.vgg19 import VGG19, preprocess_input as preprocess_vgg
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing.image import img_to_array
import joblib

class SinhalaCharacterPredictor:
    def __init__(self):
        # Load classifiers and label encoder
        self.rf = joblib.load('Models/Letter_Classify_Models/random_forest_model.pkl')
        self.et = joblib.load('Models/Letter_Classify_Models/extra_trees_model.pkl')
        self.xgb = joblib.load('Models/Letter_Classify_Models/xgboost_model.pkl')
        self.le = joblib.load('Models/Letter_Classify_Models/label_encoder.pkl')


        # Load feature extractors
        self.models = {
            'vgg19': VGG19(weights='imagenet', include_top=False, pooling='avg'),
            'inceptionv3': InceptionV3(weights='imagenet', include_top=False, pooling='avg'),
            'resnet50': ResNet50(weights='imagenet', include_top=False, pooling='avg'),
            'inceptionresnetv2': InceptionResNetV2(weights='imagenet', include_top=False, pooling='avg')
        }

        self.corrected_class_map = {
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


    def load_image(self, path):
        img = Image.open(path).convert('RGB')
        #img = ImageOps.expand(img, border=30, fill='white')
        img = img.resize((224, 224))
        return img

    def extract_features(self, image):
        image = img_to_array(image)
        if image.shape[-1] == 1:
            image = np.repeat(image, 3, axis=-1)
        image = np.expand_dims(image, axis=0)

        features = []
        for name, model in self.models.items():
            if name == 'vgg19':
                img_input = preprocess_vgg(image.copy())
            else:
                img_input = image / 255.0
            feat = model.predict(img_input, verbose=0)
            features.append(feat.flatten())
        return np.concatenate(features)

    def decode(self, label):
        return self.le.inverse_transform([label])[0]

    def predict(self, path):
        img = self.load_image(path)
        features = self.extract_features(img).reshape(1, -1)

        rf_pred = self.rf.predict(features)[0]
        et_pred = self.et.predict(features)[0]
        xgb_pred = self.xgb.predict(features)[0]

        rf_label = self.corrected_class_map.get(int(self.decode(rf_pred)))
        et_label = self.corrected_class_map.get(int(self.decode(et_pred)))
        xgb_label = self.corrected_class_map.get(int(self.decode(xgb_pred)))

        # Show image
        plt.imshow(img)
        plt.axis('off')
        plt.show()

        print(f"Predictions:\nRandom Forest: {rf_label}\nExtra Trees: {et_label}\nXGBoost: {xgb_label}")
        return rf_label, et_label, xgb_label
