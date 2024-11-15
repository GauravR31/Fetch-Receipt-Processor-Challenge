FROM python:3.8-slim

RUN apt-get update && apt-get install -y curl
WORKDIR /code

COPY . /code
RUN pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]