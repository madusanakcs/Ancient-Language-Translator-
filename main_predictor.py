from sinhala_character_predictor import SinhalaCharacterPredictor
from era_predictor import EraPredictor


class MainPredictor:
    def __init__(self, user_need="both"):
        """
        :param user_need: 'char', 'era', or 'both'
        """
        valid_needs = ["char", "era", "both"]
        if user_need not in valid_needs:
            raise ValueError(f"Invalid option for user_need. Choose from {valid_needs}")
        self.user_need = user_need
        self.char_predictor = SinhalaCharacterPredictor()
        self.era_predictor = EraPredictor()

    def predict(self, img_path):
        """
        Predict Sinhala character and/or era based on user_need.
        
        :param img_path: Path to image file
        :return: Dictionary with results based on user_need
        """
        results = {}

        if self.user_need == "char":
            predicted_char = self.char_predictor.predict(img_path)
            print(f"🧩 Predicted Character: {predicted_char}")
            results["character"] = predicted_char

        elif self.user_need == "era":
            predicted_char, predicted_era = self.era_predictor.predict_era(img_path)
            print(f"🏺 Predicted Era: {predicted_era}")
            results["character"] = predicted_char
            results["era"] = predicted_era

        elif self.user_need == "both":
            predicted_char, predicted_era = self.era_predictor.predict_era(img_path)
            print(f"🧩 Predicted Character: {predicted_char}")
            print(f"🏺 Predicted Era: {predicted_era}")
            results["character"] = predicted_char
            results["era"] = predicted_era

        return results
