import requests
import pandas as pd
import time

discount = pd.read_csv("../initial_data/discountuplift.csv", sep="\t")

feature_cols = [
    "recency",
    "history",
    "used_discount",
    "used_bogo",
    "is_referral",
    "zip_code_Rural",
    "zip_code_Surburban",
    "zip_code_Urban",
    "channel_Multichannel",
    "channel_Phone",
    "channel_Web",
]

# URL сервиса
url = "http://localhost:5000/predict"

# выполнение POST-запроса
for i in range(1000):
    print(f'requests: {i+1}')
    # пример данных для запроса
    data = {
        "features": discount[feature_cols].iloc[i].values.tolist()
    }
    response = requests.post(url, json=data)
    time.sleep(3)

    # проверка ответа
    if response.status_code == 200:
        print("Ответ сервера:", response.json())
    else:
        print("Ошибка:", response.status_code, response.text) 