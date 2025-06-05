# 🗿 Ancient Sinhala Letter Predictor 

This project is a Sinhala character and era classification tool powered by machine learning and deep learning. It uses feature extraction via pre-trained CNNs (VGG19, InceptionV3, ResNet50, etc.) and predicts characters using Random Forest, Extra Trees, and XGBoost.

---

## 🚀 Features

- Sinhala Character Recognition
- Era Classification
- Combined Prediction Output
- Ensemble Machine Learning Classifiers
- Feature Extraction from CNNs

---

## 📥 Clone the Repository

```bash
git clone https://github.com/madusanakcs/Ancient-Language-Translator-.git
cd Ancient-Language-Translator-
```
This project allows you to perform predictions on images using a pre-trained model.

## Installation

 **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can run the prediction script `use.py` with the following structure:

```python
python use.py --image_path <path_to_your_image> --prediction_type <prediction_option>
