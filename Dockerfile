# Dockerfile с переменными окружения 

FROM python:3.11-slim

RUN mkdir uplift_service

COPY . ./uplift_service
# инструкция COPY копирует содержимое текущей директории 
# (. - указывает на текущую) в директорию,
# которую указали второй командой – в данном случае это service
WORKDIR /uplift_service
# изменяем рабочую директорию Docker 
# эта команда похожа на инструкцию RUN ["cd", "./my_super_dir"]
# в документации Docker рекомендуется использовать именно WORKDIR
# в рабочей директории будут выполнены команды, указанные далее после CMD
# установим необходимые библиотеки
RUN apt-get update && apt-get install -y libgomp1
RUN pip3 install -r requirements.txt

CMD uvicorn app.main:app --reload --host  0.0.0.0 --port 5000