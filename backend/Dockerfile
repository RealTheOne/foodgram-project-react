FROM python:3.9

# WORKDIR /app
WORKDIR /foodgram

RUN apt-get update && apt-get install -y make
RUN pip install --upgrade pip
RUN pip install gunicorn==21.2.0

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["make", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "foodgram.wsgi"]