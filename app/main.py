from fastapi import FastAPI, Request, HTTPException
import pickle
import numpy as np
import uvicorn
from statsd import StatsClient
import time

# загрузите модель из файла выше
with open("./model/uplift_model.pkl", "rb") as f:
    model = pickle.load(f)

# создаём приложение FastAPI
app = FastAPI(title="uplift")

# stats_client = StatsClient(host="localhost", port=8125, prefix="uplift")
stats_client = StatsClient(host="graphite", port=8125, prefix="uplift")
    
@app.post("/predict")
async def predict(request: Request):

    # запомните время начала обработки запроса
    start_time = time.time()
    
    stats_client.incr("requests")

    # все данные передаются в json
    try:
        data = await request.json()
    except Exception as e:
        stats_client.incr("errors.invalid_json")
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    # признаки лежат в features, в массиве
    # извлекаем и преобразуем признаки
    try:
        features = data["features"]
        features = np.array(features).reshape(1, -1)
    except Exception as e:
        stats_client.incr("errors.invalid_features")
        raise HTTPException(status_code=400, detail="Invalid features format")

    # получаем предсказания
    try:
        # вероятность того, что целевое событие произойдет, если мы применим рекомендованный treatment.
        prediction = model.predict(features)[0][1]
    except Exception as e:
        stats_client.incr("errors.model_prediction")
        raise HTTPException(status_code=500, detail="Model prediction error")
                
    # посчитайте время обработки запроса в секундах как разницу 
    # между текущим временем и start_time
    response_time = time.time() - start_time

    stats_client.timing("response_time", response_time)
    stats_client.incr("response_code.200")
    stats_client.gauge("predictions", prediction)

    return {"predict": prediction.tolist()}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)