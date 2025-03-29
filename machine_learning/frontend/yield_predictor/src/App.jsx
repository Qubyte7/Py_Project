import React from "react";
import './App.css'
import axios from "axios";
import {useState} from "react";

function App() {
  const [rainfall, setRainfall] = useState("");
  const [pesticide, setPesticide] = useState("");
  const [cropType, setCropType] = useState("");
  const [average_temperature,setAverage_Temperature] = useState("")
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const handleSubmit = async (e)=>{
    e.preventDefault();
    try {
      const prediction_response = await  axios.post("http://127.0.0.1:8000/muhinzi/predict",{
        rain_fall_per_year_mm: parseFloat(rainfall),
        crop_name: cropType,
        average_temperature_per_year: parseFloat(average_temperature),
        pesticide_tonnes_per_year: parseFloat(pesticide)
      },{
        "Content-type":"application/json"
      });
      if(prediction_response.data.status_code&&prediction_response.data.status_code!=200){

        setError(prediction_response.data.message)
      }
      else{
   setPrediction(prediction_response.data)
      setError("")
      console.log(prediction_response.data)
      }

    }catch (e){
      setError(e.message);
      console.log(e.message)
      setPrediction(null);
    }
  }
  return (
      <div className="App">
        <h1>Crop Yield Prediction</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Rainfall (mm):</label>
            <input
                type="number"
                value={rainfall}
                onChange={(e) => setRainfall(e.target.value)}
                required
            />
          </div>
          <div>
            <label> average temperature :</label>
            <input
                type="number"
                value={average_temperature}
                onChange={(e) => setAverage_Temperature(e.target.value)}
                required
            />
          </div>
          <div>
            <label>Pesticide (liters):</label>
            <input
                type="number"
                value={pesticide}
                onChange={(e) => setPesticide(e.target.value)}
                required
            />
          </div>
          <div>
            <label>Crop Type:</label>
            <input
                type="text"
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                required
            />
          </div>
          <button type="submit">Predict Yield</button>
        </form>

        {error && <p style={{color: "red"}}>{error}</p>}
        {prediction !== null && (
            <p>Predicted Yield: <strong>{prediction.toFixed(2)} Hecto grams/hectare</strong></p>
        )}
      </div>
  )
}

export default App
