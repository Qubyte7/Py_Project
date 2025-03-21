import  joblib
plant_name = "Ricse"
plant_name = plant_name.capitalize()
print(plant_name)
crop_frequency_map = joblib.load("../../models/yield_predictor/crop_frequency_mapping.pkl")
print(type(plant_name))
crop_frequency = crop_frequency_map.get(plant_name)
print(crop_frequency)