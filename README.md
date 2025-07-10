# Интеграция uplift-модели в продакшен-среду.

- initial_data/discountuplift.csv - выборка с данными о целевом воздействии (предоставлении скидки) и полученном эффекте (купили товар). 
- model/uplift_model.pkl - модель для прогнозирования 'uplift_score' - вероятности того, что целевое событие произойдет, если мы применим воздействие (treatment).
- app/request.py - скрипт для тестирования микросервиса путём генерации 1000 запросов. 
- app/main.py - код микрросервиса на базе FastAPI.


## Скачайте образ Graphite из Docker Hub:
Graphite - это open-source инструмент для мониторинга и визуализации данных, основанный на временных рядах (time-series data).

```
docker pull graphiteapp/graphite-statsd
```

# Запуск контейнера с Graphite в фоновом режиме:
```
docker container run -d \
  --name graphite \
  -p 80:80 \
  -p 2003:2003 \
  -p 8125:8125/udp \
  -p 8126:8126 \
  graphiteapp/graphite-statsd
```

## Сборка образа и запуск контейнера с пользовательским микросервисом для прогнозирования 'uplift_score'

```
docker image build -t uplift-model .
docker run -p 5000:5000 --link graphite:graphite uplift-model 
```

ВАЖНО! В случае использования виртуальной машины необходимо перенаправить порты (80 И 5000) на локальный компьютер!

# Инструкции для тестирования сервисов

1) пример тестирования с использованием командной строки
```
curl -X POST -H "Content-Type: application/json" \
  -d '{"features": [10, 95.49,  0,  1,  1,  1,  0,  0,  0, 0,  1]}' \
  http://localhost:5000/predict
```

2) пример тестирования с использованием `app/request.py`
```
cd app
python request.py
```