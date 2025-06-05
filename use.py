from main_predictor import MainPredictor

img_path = "2.jpeg"
user_need = "char"  # "char", "era", or "both"

predictor = MainPredictor(user_need=user_need)
results = predictor.predict(img_path)

# Now you can access results["character"], results["era"], etc.
