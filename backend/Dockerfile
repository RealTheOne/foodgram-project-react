FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y make

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["make", "run"]