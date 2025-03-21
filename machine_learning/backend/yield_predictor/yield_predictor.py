import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# loading mode ,scaler and frequency mapp
model = joblib.load("../../models/yield_predictor/crop_yield_model.pkl")
scaler = joblib.load("../../models/yield_predictor/scaler.pkl")
crop_frequency_map = joblib.load("../../models/yield_predictor/crop_frequency_mapping.pkl")


# defining input schema
class YieldPredictorInput(BaseModel):
    rain_fall_per_year_mm: float
    crop_name: str
    average_temperature_per_year: float
    pesticide_tonnes_per_year: float


# initializing the app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["GET,POST,PUT,DELETE"],
    allow_headers=["*"],
)


# defining API
@app.post("/muhinzi/predict")
def muhinzi_predict(input_data: YieldPredictorInput):
    try:
        # map the crop name to its frequency
        plant_name = input_data.crop_name
        print(type(plant_name))
        # sanitizing plant name to work with the retrivale case sensitiviness
        plant_name = plant_name.capitalize()
        crop_frequency = crop_frequency_map.get(plant_name)
        print(crop_frequency)
        if crop_frequency is None:
            raise HTTPException(status_code=400,
                                detail="We can't predict for " + plant_name + " yet, try again later !")
        # if yes create a dataframe
        # Feature names must be in the same order as they were in fit.
        input_dataframe = pd.DataFrame({
            "crop_frequency": [crop_frequency],
            "pesticides_tonnes": [input_data.pesticide_tonnes_per_year],
            "avg_temp": [input_data.average_temperature_per_year],
            "average_rain_fall_mm_per_year": [input_data.rain_fall_per_year_mm],

        })
        # scaling the inputs
        input_dataframe_scaled = scaler.transform(input_dataframe)
        print("successfully scaled ")
        # making prediction
        prediction = model.predict(input_dataframe_scaled)
        # the return type is an array hence the prediction[0] for retrieving
        return {"Muhinzi predicted : ", prediction[0], " for " + plant_name}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str("Something went wrong during prediction " + str(e)))

# script to run this file
#  uvicorn yield_predictor
# :app --host 127.0.0.1 --port 8000 --reload
